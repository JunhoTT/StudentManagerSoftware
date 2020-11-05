function uploadFile(file, final=null) {
    getSignedRequest(file, 'post', function(response) {
        uploadFileToAWS(file, response.data, response.url, final);
    });
};

// function deleteFile(file, final=null) {
//     getSignedRequest(file, 'delete', function(response) {
//         deleteFileFromAWS(file, response.data, response.url, final);
//     });
// };

function getSignedRequest(file, method, final){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/sign_s3/"+method+"?file_name="+file.name+"&file_type="+file.type);
    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4){
            if(xhr.status === 200){
                var response = JSON.parse(xhr.responseText);
                final(response);
                // uploadFileToAWS(file, response.data, response.url, final);
            }
            else{
                alert("Could not get signed URL.");
            }
        }
    };
    xhr.send();
};

function uploadFileToAWS(file, s3Data, url, final=null){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", s3Data.url);

    var postData = new FormData();
    for(key in s3Data.fields){
        postData.append(key, s3Data.fields[key]);
    }
    postData.append('file', file);

    xhr.onreadystatechange = function() {
        if(xhr.readyState === 4){
            if(xhr.status === 200 || xhr.status === 204){
                if (final) {
                    final(url);
                }
            }
            else{
                alert("Could not upload file.");
            }
        }
    };
    xhr.send(postData);
};

// function deleteFileFromAWS(file, s3Data, url, final=null){
//     var xhr = new XMLHttpRequest();
//     xhr.open("DELETE", s3Data.url);

//     var deleteData = new FormData();
//     for(key in s3Data.fields){
//         deleteData.append(key, s3Data.fields[key]);
//     }

//     xhr.onreadystatechange = function() {
//         if(xhr.readyState === 4){
//             if(xhr.status === 200 || xhr.status === 204){
//                 if (final) {
//                     final(url);
//                 }
//             }
//             else{
//                 alert("Could not delete file.");
//             }
//         }
//     };
//     xhr.send(deleteData);
// };
