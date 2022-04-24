function courier_search() {

    if(!document.querySelector("#origin-postcode").value) {
        alert("Please enter origin post code");
        return false;
    }
    if(!document.querySelector("#destination-postcode").value) {
        alert("Please enter destination post code.");
        return false;
    }

    if(!document.querySelector("#parcel-weight").value) {
        alert("Please enter parcel weight.");
        return false;
    }

    if(!document.querySelector("#parcel-length").value) {
        alert("Please enter parcel length.");
        return false;
    }

    if(!document.querySelector("#parcel-width").value) {
        alert("Please enter parcel width.");
        return false;
    }

    if(!document.querySelector("#parcel-height").value) {
        alert("Please enter parcel height.");
        return false;
    }

    let pickUpDate = document.querySelector("#pickup_date").value;
    let deliveryDate = document.querySelector("#delivery_date").value;
    if(!pickUpDate) {
        alert("Please select pick up date.");
        return false;
    }

    if(!deliveryDate) {
        alert("Please select delivery date.");
        return false;
    }

    // if (new Date(pickUpDate) < Date.now()) {
    //     alert("The pick up date must be Bigger or Equal to today date");
    //     return false;
    // }

    if (new Date(pickUpDate) >  new Date(deliveryDate)) {
        alert("The delivery date must be Bigger or Equal pick up date");
        return false;
    }
 
    
}
