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

function deleteAllStars(stars, index, movie_id){
    for(i = 0; i <= index; i++){
        stars[i].classList.remove('checked');
    }
     $.ajax({
               url: "/movies/",
               type: 'POST',
               headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
               data: {
                        "movie_id": movie_id,
                        "rating": index + 1,
                        "delete_rating": "True",
                      },
               dataType: 'json',
               success: function(response){
                    id = ".id" + movie_id
                    average_selector = id + " .rating-average"
                    count_selector = id + " .rating-count"
                    var average_element = document.querySelector(average_selector)
                    var count_element = document.querySelector(count_selector)
                    average_element.innerHTML = response["rating_average"]
                    count_element.innerHTML = "(" + response["rating_count"] + ")"
               },
         });
}

const movie_ratings = document.querySelectorAll('.rating');
for(i = 0; i<movie_ratings.length; i++){
    const rating = movie_ratings[i]
    const stars = [...rating.querySelectorAll('.fa-star')];
    const voteHandler = (event) => {
      movie_id = rating.parentNode.id
      const selected = stars.find(e => e === event.target);
      const index = stars.indexOf(selected);
      if (!~index) {return;} // click not on a star

      if(index != 4 && selected.classList.contains('checked')
            && !(stars[index + 1].classList.contains('checked'))){

          deleteAllStars(stars, index, movie_id);

      }
      else if(index == 4 && selected.classList.contains('checked')){
           deleteAllStars(stars, index, movie_id);
      }
      else{
        stars.forEach( (e, i ) => {
        if (i <= index){
            e.classList.add('checked');

        }
        else {
            e.classList.remove('checked');
        }
      });
              $.ajax({
               url: "/movies/",
               type: 'POST',
               headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
               data: {
                        "movie_id": movie_id,
                        "rating": index + 1,
                        "delete_rating": "False",
                      },
               dataType: 'json',
               success: function(response){
                    id = ".id" + movie_id
                    average_selector = id + " .rating-average"
                    count_selector = id + " .rating-count"
                    var average_element = document.querySelector(average_selector)
                    var count_element = document.querySelector(count_selector)
                    average_element.innerHTML = response["rating_average"]
                    count_element.innerHTML = "(" + response["rating_count"] + ")"
               },
         });
      }
    }
    rating.addEventListener('click', voteHandler, false);
}

