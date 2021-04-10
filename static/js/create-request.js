window.addEventListener('DOMContentLoaded', (event) => {
    let sectorHeading = document.querySelector("#sector-name-heading");
    
    
    let dropDown = document.querySelector("#id_sector");
    updateGenreList(dropDown.value);

    dropDown.onchange = (() => {
        let selOption = dropDown.options[dropDown.selectedIndex].innerHTML;
        let selValue = dropDown.value;
      
        if (selOption !== '---------'){
            sectorHeading.innerHTML = selOption;
            sector_id_hidden.value = selValue;
            updateGenreList(selValue);
        }
    });

});


function updateGenreList(id){
    const csrftoken = getCookie('csrftoken');
    let data_ = {'sector_id':id};

    fetch('/api/list-genre/',{
        method: "POST",
        headers:{
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(data_),
    })
    .then(response => response.json())
    .then(data=>{
        let genreList = data["sector-list"];
        let selGenre = document.querySelector("#id_genre");
        let optionList = selGenre.children;
        if(optionList.length != 0){
            while (selGenre.firstChild) {
                selGenre.removeChild(selGenre.firstChild);
            }
        }
        let count = 1;
        genreList.forEach(element => {
            let newOption = document.createElement('option');
            newOption.value = count;
            newOption.innerHTML = element;
            selGenre.appendChild(newOption);
            count+=1;
        });
    });
}


// Ref: https://docs.djangoproject.com/en/3.1/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}