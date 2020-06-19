// make a data uri encoded image from a <video> element using canvas
// (thank you stackoverflow people)
function videoElementToImage(videoElement, width, height) {
    width = width || 360;
    height = height || 240;
    var canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    var context = canvas.getContext('2d');
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    var dataURI = canvas.toDataURL('image/jpeg');
    // discard created canvas element
    canvas = null;
    return dataURI;
}
// get a data uri encoded image from a video URL
function fetchVideoThumb(url, width, height) {
    width = width || 360;
    height = height || 240;
    // will be async as we need to wait some frame to be downloaded
    return new Promise(function (resolve, reject) {
        var video = document.createElement('video');
        video.width = width;
        video.height = height;
        video.attributes['preload'] = 'none';
        // first setup the listeners
        video.addEventListener('loadeddata', function () {
            var dataURI = videoElementToImage(video, width, height);
            // cleanup so loading ends
            video = null;
            // we're done, here's your thumb:
            resolve(dataURI);
        });
        video.addEventListener('error', function () {
            // remove element in case of error
            video = null;
            reject();
        });
        // then set url so load begin
        video.src = url;
    });
}


const generateThumbs = arr => {
    for (let x = 0; x < arr.length; x++) {
        const link = arr[x].link;
        if (link.includes('youtube')) {
            $(arr[x].id).attr("src", `https://img.youtube.com/vi/${youtube_parser(link)}/1.jpg`);
        } else if (link.includes('vimeo')) {
            $.ajax({
                type: 'GET',
                url: `http://vimeo.com/api/oembed.json?url=${link}`,
                jsonp: 'callback',
                dataType: 'jsonp',
                success: function (response) {
                    $(arr[x].id).attr("src", `${response.thumbnail_url}`);
                }
            });
            // $.ajax({
            //     type: "GET",
            //     url: `http://vimeo.com/api/v2/video/${vimeo_parse(link)}.json`,
            //     data: {},
            //     dataType: "json",
            //     success: function (response) {
            //         console.log($(arr[x].id))
            //         $(arr[x].id).attr("src", `${response[0].thumbnail_small}`);
            //         console.log(response[0].thumbnail_small)
            //         console.log(response)
            //     }, error: function (error) {
            //         console.log(error.responseText);
            //     }
            // });
        } else {
            fetchVideoThumb(link).then(function (thumb) {
                $(arr[x].id).attr("src", thumb);
            }, function () {
                console.log('couldnt load the video!');
            });
        }
    }
}

const youtube_parser = url => {
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url.match(regExp);
    return (match && match[7].length == 11) ? match[7] : false;
}