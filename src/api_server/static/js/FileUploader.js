let MAX_FILE_SIZE = 1073741824 //1 GB

$(function(){
    $('#file-select').change(function(e){
        //run logic to veryify
        //1. it is a CSV
        //2. not too large
        //3. is it a known data source
        /*let file = e.target.files[0];*/
        let valid = true;
        /*if(file.name.slice(file.name.lastIndexOf('.') + 1).toLowerCase() != 'csv'){
            valid = false;
            alert('This is not a csv');
        }
        if(file.size > MAX_FILE_SIZE){
            valid = false;
            alert('File size too big');
        }*/
        if(valid){
            $('#upload').prop('disabled', false);
        }
    });
    
});