document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.post_edit_button').forEach(element => {
        element.addEventListener('click', event => display(event));
    });
    document.querySelectorAll('.post_edit_save_button').forEach(element => {
        element.addEventListener('click', event => edit_save(event));
    });
    document.querySelectorAll('.image_like_heart').forEach(element => {
        element.addEventListener('click', event => like(event));
    });

    // By default, hide edit
    posts_default();
});

function posts_default(){
    document.querySelectorAll('.listing_posts_js').forEach(element => {
        element.style.display = 'block';
    });
    document.querySelectorAll('.listing_posts_edit_js').forEach(element => {
        element.style.display = 'none';
    });
    document.querySelectorAll('.listing_posts_edit_Message_All').forEach(element => {
        element.style.display = 'none';
    });
}

function display(event){
    const element = event.target;
    const post_id = element.value
    element.parentElement.style.display='none'
    document.querySelector(`.listing_posts_edit_${post_id}`).style.display = 'block';
    }


function edit_save(event) {
    const element = event.target;
    const post_id = element.value
    const link = element.dataset.path
    edited_post_text = document.querySelector(`.edit_post_textarea_${post_id}`).value 

    //https://docs.djangoproject.com/en/5.0/howto/csrf/
    //https://www.jsdelivr.com/package/npm/js-cookie (used in the layout.html)
    const csrftoken = Cookies.get('csrftoken');

    fetch(`${link}`, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body: JSON.stringify({
            newpost_text: edited_post_text
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);

        document.querySelector(`.listing_posts_edit_${post_id}`).style.display = 'none';
        document.querySelector(`.listing_posts_${post_id}`).style.display = 'block';
        document.querySelector(`.listing_posts_text_${post_id}`).innerHTML = edited_post_text;
        Alert_info = document.querySelector(`.listing_posts_edit_Message${post_id}`)
        Alert_info.style.display = 'block';
        Alert_info.innerHTML = result.success_message;
        }); 
    };

function like(event) {
    const element = event.target;
    const post_id = element.value;
    const link = element.dataset.path;
    console.log(post_id);

    const csrftoken = Cookies.get('csrftoken');
    fetch(`${link}`, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body: JSON.stringify({
            post_id: post_id 
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        if (result.hasOwnProperty('likes_num')) {
            document.querySelector(`.likes_count_${post_id}`).innerHTML = result.likes_num;
            }
        })
    .catch(() => {
        console.error("Failed to like a post ");
    });
}
