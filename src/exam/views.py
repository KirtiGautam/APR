from django.shortcuts import render, redirect
from django import http
from accounts.models import Class
from lessons.models import (Subject, question as SmallQ)
from exam.models import (exam_type, Exam, Paper, Question,
                         Answer, Option, Section, StudentAttempt, StudentPaper)
from django.utils import dateparse
from django.contrib import messages
from django.db.models import Sum, Max, Avg
import datetime
import pytz


def index(request):
    if request.user.is_authenticated:
        if request.method == "POST" and request.user.admin:
            exam = Exam.objects.create(exam_type=exam_type.objects.get(
                id=request.POST['exam_type']), Name=request.POST['exam_name'].strip(), Mode=request.POST['mode'])
            on = True if exam.Mode == "C" else False
            lis = []
            for i in range(1, int(request.POST['hidden_sn_count'])+1):
                Scheduled_on = dateparse.parse_datetime(
                    request.POST['dNt'+str(i)]).astimezone(tz=pytz.timezone("Asia/Kolkata"))
                lis.append(Paper(Subject=Subject.objects.get(id=request.POST['subject'+str(i)]), Exam=exam, Scheduled_on=Scheduled_on, Duration=request.POST['duration'+str(
                    i)], Max_Marks=request.POST['max-marks' + str(i)], Pass_Marks=request.POST['pass-marks'+str(i)], Location=request.POST['location'+str(i)], Published=on))
            Paper.objects.bulk_create(lis)
            for x in exam.Paper.all():
                StudentPaper.objects.bulk_create(
                    [StudentPaper(Student=y, Paper=x) for y in x.Subject.Class.Students.all()])
            return redirect("exam:exams")
        if request.user.admin:
            data = {
                'Exams': Exam.objects.all().distinct(),
                'types': exam_type.objects.all(),
                'classes': Class.objects.all(),
            }
        elif request.user.is_staff:
            data = {
                'Exams': Exam.objects.filter(Paper__Subject__teacher=request.user).distinct(),
            }
        else:
            data = {
                'Exams': Exam.objects.filter(Paper__Subject__Class=request.user.Student.Class).distinct(),
            }
        return render(request, 'Exam/exams.html', data)
    return redirect('accounts:login')


def examSettings(request):
    if request.user.is_authenticated and request.user.admin:
        data = {}
        if request.method == "POST":
            obj, created = exam_type.objects.get_or_create(
                Name=request.POST['exam_name'].strip())
            if created:
                return redirect('exam:exam-settings')
            data['error'] = "Exam Type already exists"
        data['exams'] = exam_type.objects.all()
        return render(request, 'settings/admin/exams/examsSettings.html', data)
    return redirect('accounts:login')


def deleteExam(request):
    if request.user.is_authenticated and request.user.admin:
        if request.method == "POST":
            exam_type.objects.filter(id=request.POST['id']).delete()
            return redirect("exam:exam-settings")
    return redirect('accounts:login')


def updateExam(request):
    if request.user.is_authenticated and request.user.admin:
        if request.method == "POST":
            exam_type.objects.filter(id=request.POST['id']).update(
                Name=request.POST['exam_name'])
            return redirect("exam:exam-settings")
    return redirect('accounts:login')


def delete(request):
    if request.user.is_authenticated and request.user.admin:
        Exam.objects.filter(id=request.POST['id']).delete()
    return redirect("exam:exams")


def papers(request, id):
    if request.user.is_authenticated:
        try:
            exam = Exam.objects.get(id=id)
        except Exception as e:
            return http.HttpResponseNotFound("No such exam exists.", e.args)
        if request.method == "POST" and request.user.admin:
            Scheduled_on = dateparse.parse_datetime(
                request.POST['scheduled']).astimezone(tz=pytz.timezone("Asia/Kolkata"))
            Paper.objects.create(Subject=Subject.objects.get(id=request.POST['subject']), Exam=exam, Scheduled_on=Scheduled_on, Duration=request.POST[
                                 'duration'], Max_Marks=request.POST['Max_Marks'], Pass_Marks=request.POST['Pass_Marks'], Location=request.POST['location'])
            return redirect('exam:papers', id=id)
        if request.user.user_type == "Student":
            paper = exam.Paper.filter(
                Subject__Class=request.user.Student.Class)
            if not paper.exists():
                return http.HttpResponseNotAllowed("Prohibhited")
        elif request.user.is_staff:
            paper = exam.Paper.filter(Subject__teacher=request.user)
            if not paper.exist():
                return http.HttpResponseNotAllowed("Prohibhited")
        else:
            paper = exam.Paper.all()
        data = {
            'exam': exam,
            'papers': paper,
            'Classes': Class.objects.all(),
        }
        return render(request, "Exam/papers.html", data)
    return redirect('accounts:login')


def editPaper(request, id):
    if request.user.is_authenticated:
        if request.user.user_type == "Student":
            return http.HttpResponseForbidden("Not Alowed")
        try:
            paper = Paper.objects.get(id=id)
        except Exception as e:
            return http.HttpResponseNotFound("No such paper", e.args)
        if paper.Scheduled_on < datetime.datetime.now(pytz.utc):
            messages.error(request, "Cannot edit after Scheduled time")
            return redirect('exam:papers', id=paper.Exam.id)
        if request.method == "POST":
            if request.POST['QType'] == "O":
                question = Question.objects.create(Paper=paper, Correct=request.POST['max_marks'], SNo=request.POST['QSNo'], Text=request.POST[
                                                   'Question-text'], Type=request.POST['QType'], Incorrect=request.POST['Incorrect'], Unattempted=request.POST['unattempted'])
                if 'Question-Image' in request.FILES:
                    question.Asset = request.FILES['Question-Image']
                    question.save()
                for x in range(1, 5):
                    option = Option.objects.create(
                        Question=question, Text=request.POST['op'+str(x)+'-text'])
                    if 'op'+str(x)+'-file' in request.FILES:
                        option.Asset = request.FILES['op'+str(x)+'-file']
                        option.save()
                    if int(request.POST['correct-option']) == x:
                        ans = Answer.objects.create(
                            Question=question, Option=option, Explanation=request.POST['correct-explanation'])
                        if 'exp-file' in request.FILES:
                            ans.Asset = request.FILES['exp-file']
                        ans.save()
            elif request.POST['QType'] == "S":
                question = Question.objects.create(Paper=paper, Correct=request.POST['max_marks'], SNo=request.POST['QSNo'], Text=request.POST[
                                                   'short-Question-text'], Type=request.POST['QType'], Incorrect=request.POST['Incorrect'], Unattempted=request.POST['unattempted'])
                if 'short-Question-file' in request.FILES:
                    question.Asset = request.FILES['short-Question-file']
                    question.save()
                Answer.objects.create(
                    Question=question, Explanation=request.POST['short-Question-answer'])
            elif request.POST['QType'] == "L":
                question = Question.objects.create(Paper=paper, Correct=request.POST['max_marks'], SNo=request.POST['QSNo'], Text=request.POST[
                                                   'long-Question-text'], Type=request.POST['QType'], Incorrect=request.POST['Incorrect'], Unattempted=request.POST['unattempted'])
                if 'long-Question-file' in request.FILES:
                    question.Asset = request.FILES['long-Question-file']
                    question.save()
                Answer.objects.create(
                    Question=question, Explanation=request.POST['long-Question-answer'])
            else:
                joined = "','".join([request.POST['fill-question'+str(x
                                                                      )]
                                     for x in range(1, int(request.POST['hidden-fill-count'])+1)])
                question = Question.objects.create(Paper=paper, Correct=request.POST['max_marks'], SNo=request.POST['QSNo'], Text=request.POST[
                                                   'fill-question'], Type=request.POST['QType'], Incorrect=request.POST['Incorrect'], Unattempted=request.POST['unattempted'])
                if 'fill-question-file' in request.FILES:
                    question.Asset = request.FILES['fill-question-file']
                    question.save()
                Answer.objects.create(Question=question, Explanation=joined)
            return redirect("exam:edit-paper", id=id)
        sum = paper.Question.all().aggregate(Sum("Correct"))['Correct__sum']
        data = {
            'paper': paper,
            'marks_till_now': paper.Max_Marks - sum if sum else paper.Max_Marks,
            'db_q': SmallQ.objects.filter(Lesson__Subject=paper.Subject)
        }
        return render(request, 'Exam/paperEdit.html', data)
    return redirect('accounts:login')


def deleteQuestion(request, id):
    if request.user.is_authenticated:
        if request.user.user_type == "Student":
            return http.HttpResponseForbidden("Forbidden")
        question = Question.objects.get(id=id)
        paper = question.Paper.id
        question.delete()
        return redirect('exam:edit-paper', id=paper)
    return redirect('accounts:login')


def editQuestion(request):
    if request.user.is_authenticated and request.user.user_type != "Student":
        if request.method == "POST":
            question = Question.objects.get(
                id=request.POST['edit-question-id'])
            question.SNo = request.POST['edit-QSNo']
            question.Correct = request.POST['edit-max_marks']
            question.Incorrect = request.POST['edit-incorrect']
            question.Unattempted = request.POST['edit-unattempted']
            if question.Type == "O":
                question.Text = request.POST['edit-Question-text']
                if 'edit-Question-Image' in request.FILES:
                    question.Asset = request.FILES['edit-Question-Image']
                for x in range(1, 5):
                    option = Option.objects.get(
                        id=request.POST['hidden-edit-op'+str(x)])
                    option.Text = request.POST['edit-op'+str(x)+'-text']
                    if 'edit-op'+str(x)+'-file' in request.FILES:
                        option.Asset = request.FILES['edit-op'+str(x)+'-file']
                    option.save()
                    if int(request.POST['edit-correct-option']) == option.id:
                        ans = Answer.objects.get(
                            id=request.POST['hidden-edit-ob-answer'])
                        ans.Option = option
                        ans.Explanation = request.POST['edit-correct-explanation']
                        if 'edit-exp-file' in request.FILES:
                            ans.Asset = request.FILES['edit-exp-file']
                        ans.save()
            elif question.Type == "S":
                question.Text = request.POST['edit-short-Question-text']
                if 'edit-short-Question-file' in request.FILES:
                    question.Asset = request.FILES['edit-short-Question-file']
                    question.save()
                Answer.objects.filter(id=request.POST['edit-short-Answer-id']).update(
                    Explanation=request.POST['edit-short-Question-answer'])
            elif question.Type == "L":
                question.Text = request.POST['edit-long-Question-text']
                if 'edit-long-Question-file' in request.FILES:
                    question.Asset = request.FILES['editlong-Question-file']
                    question.save()
                Answer.objects.filter(id=request.POST['edit-long-Answer-id']).update(
                    Explanation=request.POST['edit-long-Question-answer'])
            else:
                joined = "','".join([request.POST['edit-fill-question'+str(x)]
                                     for x in range(1, int(request.POST['edit-hidden-fill-count'])+1)])
                question.Text = request.POST['edit-fill-question']
                if 'edit-fill-question-file' in request.FILES:
                    question.Asset = request.FILES['edit-fill-question-file']
                    question.save()
                Answer.objects.filter(
                    id=request.POST['edit-fill-answer-id']).update(Explanation=joined)
            question.save()
            return redirect("exam:edit-paper", id=question.Paper.id)
        question = Question.objects.get(id=request.GET['id'])
        data = {
            'id': question.id,
            'SNo': question.SNo,
            'Text': question.Text,
            'Max_Marks': question.Correct,
            'incorrect': question.Incorrect,
            'unattempted': question.Unattempted,
            'Asset': question.Asset.url if question.Asset else None,
            'Type': question.Type,
        }
        if question.Type == 'O':
            data['options'] = list(
                question.Option.all().values('id', 'Text', 'Asset'))
            data['Answer'] = {
                'id': question.Answer.id,
                'Explanation': question.Answer.Explanation,
                'Option': question.Answer.Option.id,
            }
        elif question.Type == 'S' or question.Type == 'L':
            data['Answer'] = {
                'id': question.Answer.id,
                'Explanation': question.Answer.Explanation,
            }
        else:
            data['Answer'] = {
                'id': question.Answer.id,
                'blanks': question.Answer.get_blanks(),
            }
        if question.Answer.Asset:
            data['Answer']['asset'] = question.Answer.Asset.url
        return http.JsonResponse(data)
    return http.HttpResponseForbidden("Not Allowed")


def markQuestion(request):
    if request.user.is_authenticated and request.user.user_type != "Student":
        paper = Paper.objects.get(id=request.POST['id'])
        paper.File = not paper.File
        paper.save()
        return http.JsonResponse("Marked as File Submission" if paper.File else "Mark as File Submission", safe=False)
    return http.HttpResponseForbidden("Not Allowed")


def addSection(request):
    if request.user.is_authenticated and request.user.user_type != "Student":
        paper = Paper.objects.get(id=request.POST['hidden_section_paper_id'])
        Section.objects.create(
            Paper=paper, Start=request.POST['start_number'], End=request.POST['end_number'])
        return redirect("exam:edit-paper", id=paper.id)
    return http.HttpResponseForbidden("Not Allowed")


def editSection(request, id):
    if request.user.is_authenticated and request.user.user_type != "Student":
        section = Section.objects.get(id=id)
        section.Start = request.POST['start_number'+str(section.id)]
        section.End = request.POST['end_number'+str(section.id)]
        section.save()
        return redirect("exam:edit-paper", id=section.Paper.id)
    return http.HttpResponseForbidden("Not Allowed")


def finishPaper(request, id):
    if request.user.is_authenticated and request.user.user_type != "Student":
        paper = Paper.objects.get(id=id)
        if not paper.Published:
            ser = 0
            if paper.Question.all().count() < 1:
                messages.error(request, "Please add at least one Question")
                return redirect('exam:edit-paper', id=paper.id)
            if paper.Section.all().count() < 1:
                messages.error(request, "Please add at least one Section")
                return redirect('exam:edit-paper', id=paper.id)
            marks = 0
            for x in paper.Question.all().order_by('SNo'):
                ser += 1
                marks += x.Correct
                if ser != x.SNo:
                    messages.error(
                        request, "Question numbers are not consecutive")
                    return redirect('exam:edit-paper', id=paper.id)
            if marks != paper.Max_Marks:
                messages.error(request, "Marks sum is not equal to Max Marks")
                return redirect('exam:edit-paper', id=paper.id)
            sections = paper.Section.all()
            for section in sections:
                if section.Start < 0 or section.End > ser:
                    messages.error(request, "Section range is improper")
                    return redirect('exam:edit-paper', id=paper.id)
                for d in sections:
                    if d.id != section.id and ((section.Start in range(d.Start, d.End+1) or (section.End in range(d.Start, d.End+1)))):
                        messages.error(request, "Sections are overlapping")
                        return redirect('exam:edit-paper', id=paper.id)
            paper.Published = not paper.Published
            paper.save()
            lis = []
            for x in paper.Subject.Class.Students.all():
                for y in paper.Question.all():
                    lis.append(StudentAttempt(Student=x, Question=y))
            StudentAttempt.objects.bulk_create(lis)
        return redirect('exam:edit-paper', id=paper.id)
    return http.HttpResponseForbidden("Not Allowed")


def instruction(request, id):
    if request.user.is_authenticated and request.user.user_type == "Student":
        return render(request, 'Exam/instruction.html', {'id': id})
    return http.HttpResponseForbidden("Not Allowed")


def studentPaper(request, id):
    if request.user.is_authenticated and request.user.user_type == "Student":
        try:
            paper = Paper.objects.get(id=id)
        except Exception as e:
            return http.HttpResponseNotFound("Not Found", e.args)
        now = datetime.datetime.now(pytz.utc)
        if now < paper.Scheduled_on or now > (paper.Scheduled_on+datetime.timedelta(minutes=paper.Duration)) or not paper.Published:
            messages.warning(
                request, "Exam can only be given in the mentioned time period")
            return redirect('exam:papers', id=paper.Exam.id)
        if not paper.Published:
            messages.warning(request, "Paper not published, contact Admin")
            return redirect('exam:papers', id=paper.Exam.id)
        attempt = StudentPaper.objects.get(
            Student=request.user.Student, Paper=paper)
        if attempt.Done:
            messages.warning(request, "Cannot give exam once finished")
            return redirect('exam:papers', id=paper.Exam.id)
        if request.method == "POST":
            if 'finissh' in request.POST:
                if not paper.File and paper.pattern() == 'Objective':
                    attempt.Marks = StudentAttempt.objects.aggregate(Sum('Marks'))[
                        'Marks__sum']
                    attempt.Checked = True
                attempt.Done = True
                attempt.save()
                return http.JsonResponse("Marked as done", safe=False)
            elif paper.File:
                attempt.File = request.FILES['file-submission']
                attempt.save()
                return http.JsonResponse(request.build_absolute_uri(attempt.File.url), safe=False)
            else:
                question = Question.objects.get(
                    id=request.POST['hidden_question_id'])
                obj = StudentAttempt.objects.get(
                    Student=request.user.Student, Question=question)
                if question.Type == "O":
                    obj.Option = Option.objects.get(
                        id=request.POST['student-option-response']) if 'student-option-response' in request.POST else None
                    if obj.Option and question.Answer.Option == obj.Option:
                        obj.Marks = question.Correct
                    else:
                        obj.Marks = question.Incorrect
                elif question.Type == "S":
                    obj.Text = request.POST['short-Answer'] if 'short-Answer' in request.POST else None
                elif question.Type == "L":
                    obj.Text = request.POST['long-answer'] if 'long-answer' in request.POST else None
                else:
                    answer = "','".join([request.POST['blank'+str(x)] if 'blank'+str(
                        x) in request.POST else None for x in range(1, len(question.Answer.get_blanks())+1)])
                    obj.Text = answer
                obj.save()
                response = redirect("exam:paper", id=id)
                response['Location'] += '?section='+request.GET['section'] + \
                    '&question=' + \
                    (request.POST['next']
                     if 'next' in request.POST else request.POST['prev'])
                return response
        time = paper.Scheduled_on+datetime.timedelta(minutes=paper.Duration)
        if paper.File:
            questions = paper.Question.all()
            section = None
        else:
            section = paper.Section.all()[int(request.GET['section'])]
            questions = paper.Question.filter(
                SNo__gte=section.Start, SNo__lte=section.End)
        data = {
            'paper': paper,
            'questions': questions.order_by('SNo'),
            'Question': questions[int(request.GET['question'])],
            'Section': section,
            'Time': time,
            'attemp': attempt,
        }
        return render(request, 'Exam/studentexam.html', data)
    return http.HttpResponseForbidden("Not Allowed")


def clearQuestion(request, id):
    if request.user.is_authenticated and request.user.user_type == "Student":
        question = Question.objects.get(id=id)
        if question.Student.filter(user=request.user).exists():
            question.Student.remove(request.user.Student)
            question.save()
        response = redirect("exam:paper", id=question.Paper.id)
        response['Location'] += '?section='+request.GET['section'] + \
            '&question='+request.GET['question']
        return response
    return http.HttpResponseForbidden("Not Allowed")


def finishExam(request):
    if request.user.is_authenticated and request.user.user_type == "Student":
        return render(request, 'Exam/examfinish.html')
    return http.HttpResponseForbidden("Not Allowed")


def offlineGrade(request, id):
    if request.user.is_authenticated and request.user.user_type != "Student":
        try:
            paper = Paper.objects.get(id=id)
        except Exception as e:
            return http.Http404("Not found", e.args)
        if request.method == 'POST':
            for x in range(1, int(request.POST['hidden_count_student'])):
                marks = int(
                    request.POST['marks'+str(x)]) if request.POST['marks'+str(x)] != '' else None
                StudentPaper.objects.filter(id=int(
                    request.POST['hidden_marks'+str(x)])).update(Marks=marks)
            return redirect('exam:result-offline', id=paper.id)
        students = [StudentPaper.objects.get(
            Student=x, Paper=paper) for x in paper.Subject.Class.Students.all()]
        data = {
            'paper': paper,
            'students':  sorted(students, key=lambda x: (x.Marks is None, x.Marks), reverse=True),
            'count': len(students)+1
        }
        return render(request, 'Exam/offlineresult.html', data)
    return redirect("accounts:login")


def onlineGrade(request, id):
    if request.user.is_authenticated and request.user.user_type != "Student":
        try:
            paper = Paper.objects.get(id=id)
        except Exception as e:
            return http.Http404("Not found", e.args)
        students = [StudentPaper.objects.get(
            Student=x, Paper=paper) for x in paper.Subject.Class.Students.all()]
        data = {
            'pending': [x for x in students if not x.Checked],
            'completed': [x for x in students if x.Checked],
            'paper': paper
        }
        return render(request, 'Exam/onlineresult.html', data)
    return redirect("accounts:login")


def GradeFile(request, id):
    if request.user.is_authenticated and request.user.user_type != "Student":
        attempt = StudentPaper.objects.get(id=id)
        if not attempt.Paper.File:
            messages.error(request, "Paper is not file type")
            return redirect("exam:result-online", id=attempt.Paper.id)
        if request.method == 'POST':
            if request.POST['Marks']:
                attempt.Marks = request.POST['Marks']
                attempt.Checked = True
                attempt.save()
            return redirect('exam:grade-online', id=id)
        data = {
            'attempt': attempt
        }
        return render(request, 'Exam/fileResult.html', data)
    return redirect("accounts:login")


def Grade(request, id):
    if request.user.is_authenticated and request.user.user_type != "Student":
        attempt = StudentPaper.objects.get(id=id)
        if attempt.Paper.File:
            messages.error(request, "Paper is File type")
            return redirect("exam:result-online", id=attempt.Paper.id)
        if request.method == 'POST':
            count = 0
            flag = True
            for x in range(int(request.POST['hidden_question_count'])):
                attemp = StudentAttempt.objects.get(
                    id=request.POST['hidden_attempt_id'+str(x)])
                attemp.Marks = int(
                    request.POST['score'+str(x)]) if request.POST['score'+str(x)] else None
                attemp.save()
                if not request.POST['score'+str(x)]:
                    flag = False
                count += attemp.Marks if attemp.Marks else 0
            attempt.Marks = count
            attempt.Checked = flag
            attempt.save()
            return redirect('exam:Grade-online', id=id)
        questAttempts = []
        for x in attempt.Paper.Question.all():
            stu = StudentAttempt.objects.get(
                Student=attempt.Student, Question=x)
            if stu.Marks is None:
                stu.Marks = stu.Question.Unattempted
                stu.save()
            questAttempts.append(stu)
        data = {
            'attempt': attempt,
            'attempts': questAttempts,
            'allatt': StudentPaper.objects.filter(Paper=attempt.Paper)
        }
        return render(request, 'Exam/multiresult.html', data)
    return redirect("accounts:login")


def publishResult(request):
    if request.user.is_authenticated and request.user.user_type != "Student":
        paper = Paper.objects.get(id=request.POST['id'])
        if not paper.Result and StudentPaper.objects.filter(Paper=paper, Marks__isnull=True).exists():
            return http.HttpResponseBadRequest("Please Grade all Students before publishing results")
        paper.Result = not paper.Result
        paper.save()
        return http.JsonResponse("UnPublish Result" if paper.Result else "Publish Result", safe=False)
    return http.HttpResponseForbidden("Not allowed")


def publishExam(request):
    if request.user.is_authenticated and request.user.user_type != "Student":
        exam = Exam.objects.get(id=request.POST['id'])
        if not exam.Result and exam.Paper.filter(Result=False).exists():
            return http.HttpResponseBadRequest("Please Grade all Students before publishing Exam")
        exam.Result = not exam.Result
        exam.save()
        return http.JsonResponse("UnPublish Exam Result" if exam.Result else "Publish Exam Result", safe=False)
    return http.HttpResponseForbidden("Not allowed")


def Results(request, id):
    if request.user.is_authenticated and request.user.user_type == "Student":
        exam = Exam.objects.get(id=id)
        papers = exam.Paper.all()
        cards = []
        for x in papers:
            student = StudentPaper.objects.get(
                Student=request.user.Student, Paper=x)
            if not student.Marks:
                student.Marks = 0
                student.save()
            cards.append({
                'paper': x,
                'student': student,
                'Topper': StudentPaper.objects.filter(Paper=x).aggregate(Max('Marks'))['Marks__max'],
                'Average': StudentPaper.objects.filter(Paper=x).aggregate(Avg('Marks'))['Marks__avg'],
            })
        stus = []
        from accounts.models import Student as s
        for x in papers:
            for y in s.objects.filter(Class=request.user.Student.Class, user__status='A'):
                stubP = StudentPaper.objects.get(Paper=x, Student=y)
                if stubP.Marks is None:
                    stubP.Marks = 0
                    stubP.save()
        for x in s.objects.filter(Class=request.user.Student.Class, user__status='A'):
            stus.append({
                'stud': x,
                's': StudentPaper.objects.filter(Paper__Exam=exam, Student=x).aggregate(Sum('Marks'))['Marks__sum'],
            })
            if x.user == request.user:
                fail = False
                for y in StudentPaper.objects.filter(Paper__Exam=exam, Student=x):
                    if y.Marks < y.Paper.Pass_Marks:
                        fail = True
                mine = {
                    's': StudentPaper.objects.filter(Paper__Exam=exam, Student=x).aggregate(Sum('Marks'))['Marks__sum'],
                    'failed': fail
                }
        stus = sorted(stus, key=lambda x: (
            x['s'] is None, x['s']), reverse=True)
        for x in range(len(stus)):
            if stus[x]['stud'].user == request.user:
                mine['rank'] = x+1
        data = {
            'exam': exam,
            'cards': cards,
            'Max': exam.Paper.aggregate(Sum('Max_Marks'))['Max_Marks__sum'],
            'studens': stus,
            'Mine': mine,
            'aver': sum([x['s'] for x in stus])/len(stus),
        }
        return render(request, 'Exam/studentResult.html', data)
    return redirect("accounts:login")


def proctored(request):
    if request.user.is_authenticated and request.user.user_type != "Student":
        paper = Paper.objects.get(id=request.POST['id'])
        paper.Proctored = not paper.Proctored
        paper.save()
        return http.JsonResponse('Mark as UnProctored Exam' if paper.Proctored else 'Mark as Proctored Exam', safe=False)
    return http.HttpResponseForbidden("Not allowed")


def importQuestions(request):
    if request.user.is_authenticated and request.user.user_type != "Student":
        paper = Paper.objects.get(id=request.POST['db_paper_id'])
        for x in range(int(request.POST['db_paper_counter'])):
            if 'check'+str(x) in request.POST:
                if request.POST['checkval'+str(x)]:
                    sum = paper.Question.all().aggregate(
                        Sum("Correct"))['Correct__sum']
                    sum = paper.Max_Marks - sum if sum else paper.Max_Marks
                    if sum < int(request.POST['checkval'+str(x)]):
                        messages.error(
                            request, "Error: Cannot import, Marks exceed Max Marks " + str(x+1))
                        break
                    ques = SmallQ.objects.get(
                        id=int(request.POST['check'+str(x)]))
                    no = paper.Question.all().order_by('SNo').last()
                    no = no.SNo+1 if no else 1
                    Ques = Question.objects.create(Paper=paper, Correct=int(request.POST['checkval'+str(x)]), Incorrect=int(
                        request.POST['inc'+str(x)]), Unattempted=int(request.POST['unam'+str(x)]), Type='O', SNo=no, Text=ques.Name)
                    for x in ques.choice.all():
                        opt = Option.objects.create(Question=Ques, Text=x.Name)
                        if x == ques.Answer.choice:
                            Answer.objects.create(
                                Question=Ques, Option=opt, Explanation=ques.Answer.explanation)
                else:
                    messages.error(
                        request, "Error: Cannot import, No marks defined in Question " + str(x+1))
                    break
        return redirect('exam:edit-paper', id=paper.id)
    return http.HttpResponseForbidden("Not allowed")


def faultCounter(request):
    if request.user.is_authenticated and request.user.user_type == "Student":
        attempt = StudentPaper.objects.get(id=request.POST['id'])
        attempt.Faults += 1
        attempt.save()
        return http.JsonResponse("Done", safe=False)
    return http.HttpResponseForbidden("Not allowed")


def paperDetails(request):
    if request.user.is_authenticated and request.user.admin:
        if request.method == 'POST':
            paper = Paper.objects.get(id=request.POST['id'])
            print(request.POST)
            Scheduled_on = dateparse.parse_datetime(
                request.POST['scheduled']).astimezone(tz=pytz.timezone("Asia/Kolkata"))
            paper.Scheduled_on = Scheduled_on
            paper.Duration = request.POST['duration']
            paper.Max_Marks = request.POST['Max_Marks']
            paper.Pass_Marks = request.POST['Pass_Marks']
            paper.save()
            return redirect('exam:papers', id=paper.Exam.id)
        paper = Paper.objects.get(id=request.GET['id'])
        return http.JsonResponse(({
            'id': paper.id,
            'Scheduled_on': paper.Scheduled_on,
            'Duration': paper.Duration,
            'Max_Marks': paper.Max_Marks,
            'Pass_Marks': paper.Pass_Marks,
        }))
    return redirect('accounts:login')


def paperDelete(request):
    if request.user.is_authenticated and request.user.admin:
        paper = Paper.objects.get(id=request.POST['id'])
        id = paper.Exam.id
        paper.delete()
        return redirect('exam:papers', id=id)
