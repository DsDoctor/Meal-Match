// alert('error');
let card_list = document.getElementById("homepage_card");
const homepage_card_length = card_list.length;
for (let s = 0; s < homepage_card_length;s++){
    card_list[0].remove();
}

    fetch(apiUrl + "/user",{
        method : "GET",
        headers: new Headers({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    })
        .then(res => res.json())
        .catch(error => console.error('Error:', error))
        .then(function (res) {
            create_card(res);
        });



function create_card(res) {
    try {
        // <!--    <div class="card-deck">-->
        let card_deck = document.createElement("div");
        card_deck.className="card-deck";
        for (let i = 0; i < res.card.length; i++) {

            // <!--        <div class="card">-->
            // <!--            <img src="{{card_1_img_link}}" class="card-img-top" alt="...">-->
            // <!--            <div class="card-body">-->
            // <!--                <h5 class="card-title">{{card_1_title}}</h5>-->
            // <!--                <p class="card-text">This is a longer card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>-->
            // <!--                <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>-->
            // <!--            </div>-->
            // <!--        </div>-->

            card_deck.innerHTML("<div class=\"card\">" +
                "<img src= " + res.card[1] + " class=\"card-img-top\" alt=\"...\">" +
                "<div class=\"card-body\">" +
                "<h5 class=\"card-title\"> "+ res.card[2] +" </h5>"
            )
        }
    }
    catch (TypeError) {

    }
}
