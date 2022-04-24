document.addEventListener("DOMContentLoaded", () => {

    filter_price();
    document.querySelector(".clr-filter-div button").addEventListener('click', reset_filter);

});
 
function filter_insurance(element=null) {
    filter_price();
    if (element) {
        inactive(element);
        active(element);   
    }
    
    let couriers = null;
    if (true) {
        if(document.querySelector(".insurance-filter-slot-group .square-box.active")) {
            start = document.querySelector(".insurance-filter-slot-group .square-box.active").dataset.start;
            couriers = document.querySelectorAll("#outcome_div .courier-div-box.show");
        }
        showhide_insurance(couriers, start);
    }
}

function filter_reDelivery(element=null) {
    filter_price();
    if (element) {
        inactive(element);
        active(element);   
    }

    let couriers = null;
    if (true) {
        if(document.querySelector(".redelivery-filter-slot-group .square-box.active")) {
            start = document.querySelector(".redelivery-filter-slot-group .square-box.active").dataset.start;
            couriers = document.querySelectorAll("#outcome_div .courier-div-box.show");
        }
        showhide_redelivery(couriers, start);
    }
}


function showhide_redelivery(couriers, start) {
    if (couriers) {
        for (let i = 0; i < couriers.length; i++) {
            reDelivery = couriers[i].querySelector(".courier-homeDelivery h6").innerText;
            if (start == 0){
                if(reDelivery.toLowerCase() === "yes") {
                    couriers[i].classList.add('show');
                    couriers[i].classList.remove('hide');
                }
                else {
                    couriers[i].classList.add('hide');
                    couriers[i].classList.remove('show');
                }
            } 
            else {
                if(reDelivery.toLowerCase() === "no") {
                    couriers[i].classList.add('show');
                    couriers[i].classList.remove('hide');
                }
                else {
                    couriers[i].classList.add('hide');
                    couriers[i].classList.remove('show');
                }
            }

        }
    }
}

function showhide_insurance(couriers, start) {
    if (couriers) {
        for (let i = 0; i < couriers.length; i++) {
            insurance = couriers[i].querySelector(".courier-insurance h6").innerText;
            if (start == 0){
                if(insurance.toLowerCase() === "yes") {
                    couriers[i].classList.add('show');
                    couriers[i].classList.remove('hide');
                }
                else {
                    couriers[i].classList.add('hide');
                    couriers[i].classList.remove('show');
                }
            } 
            else {
                if(insurance.toLowerCase() === "no") {
                    couriers[i].classList.add('show');
                    couriers[i].classList.remove('hide');
                }
                else {
                    couriers[i].classList.add('hide');
                    couriers[i].classList.remove('show');
                }
            }

        }
    }
}

function active(slot) {
    slot.classList.add('active');
    slot.querySelectorAll('img').forEach(image => {
        if(image.dataset.statefor === 'inactive') {
            image.style.display = 'none';
        }
        else {
            image.style.display = 'block';
        }
    });
}

function inactive(slot) {
    if (slot) {
        slot.parentElement.querySelectorAll('.active').forEach(element => {
            element.classList.remove('active');
            element.querySelectorAll('img').forEach(image => {
                if(image.dataset.statefor === 'inactive') {
                    image.style.display = 'block';
                }
                else {
                    image.style.display = 'none';
                }
            })
        });
    }
}

function filter_price() {
    let value = document.querySelector(".filter-price input[type=range]").value;
    document.querySelector(".filter-price .final-price-value").innerText = value;

    let div = document.querySelector("#outcome_div");
    let couriers = div.querySelectorAll(".courier-div-box");
    for (let i = 0; i < couriers.length; i++) {
        if (couriers[i].querySelector(".courier-price span").innerText > parseInt(value)) {
            couriers[i].classList.add('hide');
            couriers[i].classList.remove('show');
        }
        else {
            couriers[i].classList.add('show');
            couriers[i].classList.remove('hide');
        }
    }
    
}

function reset_filter() {
    document.querySelectorAll('.filter-slot').forEach(slot => {
        inactive(slot.querySelector(".square-box.active"));
    });
    let max = document.querySelector(".filter-price input[type=range]").getAttribute('max');
    document.querySelector(".filter-price input[type=range]").value = max;
    document.querySelector(".filter-price .final-price-value").innerText = max;

    let couriers = document.querySelector("#outcome_div").querySelectorAll(".courier-div-box");
    for (let i = 0; i < couriers.length; i++) {
            couriers[i].classList.add('show');
            couriers[i].classList.remove('hide');
    }
}



