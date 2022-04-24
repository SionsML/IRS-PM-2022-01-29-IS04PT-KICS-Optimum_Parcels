document.addEventListener("DOMContentLoaded", () => {
    let check = [false,false,false,false,false,false];
    document.querySelectorAll(".userInputs").forEach(input => {
        input.addEventListener('input', () => {

            if(input.classList.contains('user_name')){
                if(input.value.trim().length !== 0) {check[0]=true;}
                else{check[0] = false;}
            }
            if(input.classList.contains('first_name')){
                if(input.value.trim().length !== 0) {check[1]=true;}
                else{check[1] = false;}
            }
            if(input.classList.contains('last_name')){
                if(input.value.trim().length !== 0) {check[2]=true;}
                else{check[2] = false;}
            }
            if(input.classList.contains('password')){
                document.querySelector('.confirm_password').value = "";
                document.querySelector('.confirm_password').parentElement.querySelector('span').innerText = "";
                check[4] = false;
                if(input.value.trim().length !== 0) {check[3]=true;}
                else{check[3] = false;}
            }
            if(input.classList.contains('confirm_password')){
                if(input.value.trim().length !== 0) {
                    if(input.value !== document.querySelector('.password').value) {
                        input.parentElement.querySelector('span').innerText = "Password must match";
                        check[4] = false;
                    }
                    else {
                        input.parentElement.querySelector('span').innerText = "";
                        check[4]=true;
                    }
                }
                else{check[4] = false;}
            }
            if(input.classList.contains('email')){
                if(input.value.trim().length !== 0) {check[5]=true;}
                else{check[5] = false;}
            }

            let i;
            for(i=0;i<6;i++) {
                if(!check[i]) {
                    break;
                }
            }

            if(i===6) {
                document.querySelector('input[type="submit"]').disabled = false;
            }
            else {
                document.querySelector('input[type="submit"]').disabled = true;
            }

        });
    });
});