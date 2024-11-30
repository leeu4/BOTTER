const pass_input = document.getElementById("floatingPassword");
const email_input = document.getElementById("floatingEmail");
const username_input = document.getElementById("floatingUsername");
const show_link = document.getElementById("show_pass");
const button = document.getElementById("button");
const body = document.getElementById("boody");

show_link.addEventListener("click",()=>{
    if(pass_input.type == "password"){
        pass_input.type="text";
    }
    else{
        pass_input.type="password";
    }
})
const form = document.getElementById("form");
form.addEventListener("submit",async(e)=>{
    e.preventDefault();
    button.className="btn btn-primary form-control";
    button.setAttribute("type","button");
    button.setAttribute("disabled",true);
    button.innerHTML = `
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>`

    const request = await fetch("http://127.0.0.1:3000/register",{
        method:"POST",
        headers:{"Content-type":"application/json"},
        body:(JSON.stringify({
            "username":username_input.value,
            "email":email_input.value,
            "password":pass_input.value,
        }))
    })
    const data = await request.json();
    if(request.ok){
        button.className="btn btn-primary form-control";
        button.removeAttribute("type")
        button.removeAttribute("disabled")
        button.innerHTML = "Submit";
        const alert = document.createElement("div");
        alert.className="alert alert-success";
        alert.setAttribute("role","alert");
        alert.innerHTML = data.message;
        console.log("Ok")
        body.append(alert)
        alert.style="position:absolute;top:0;"
        setInterval(()=>{
            body.removeChild(alert)
            location.href="../login/index.html"
        },2000)
    }
    else{
        button.className="btn btn-primary form-control";
        button.removeAttribute("type")
        button.removeAttribute("disabled")
        console.log("Not ok")
        button.innerHTML = "Submit";
        const alert = document.createElement("div");
        alert.className="alert alert-danger";
        alert.setAttribute("role","alert");
        alert.innerHTML = data.message;
        body.append(alert)
        alert.style="position:absolute;top:0;"
        setInterval(()=>{
            body.removeChild(alert)
        },2000)
    }
    
})
