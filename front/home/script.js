const buttons_container = document.getElementById("buttons_container");
window.addEventListener('load',()=>{
    if(localStorage.getItem("name") != undefined || localStorage.getItem("name") != null){
        buttons_container.innerHTML = `
        <div class="dropdown" id="UserButton">
  <button class="btn btn-primary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
    ${localStorage.getItem("name")}
  </button>
  <ul class="dropdown-menu">
    <li><a class="dropdown-item" href="#">Profile</a></li>
    <li><a class="dropdown-item bg-danger text-white" href="#" onclick="logout()">Logout</a></li>
  </ul>
</div>`
    }
})
function logout(){
    localStorage.clear();
    window.location.reload();

}
const Search_btn = document.getElementById("Search_btn");
Search_btn.addEventListener("click",async()=>{
    const table_body = document.getElementById("tbody");
    table_body.innerHTML = ""
    const request = await fetch("http://127.0.0.1:3000/search",{
        headers:{"Content-type":"application/json","authorization":localStorage.getItem("token")}
    })
    const data = await request.json();
    data.forEach(product => {
        const new_row = document.createElement('tr');
        const name_elem = document.createElement("td");
        name_elem.innerHTML = `<td>${product.name}</td>`
        const is_instock = document.createElement("td");
        console.log(product.isinstock)
        if(product.isinstock == true){
            is_instock.innerHTML = `<td><i class="fa-solid fa-check"></i></td>`
        }
        else{
            is_instock.innerHTML = `<td><i class="fa-solid fa-xmark"></i></td>`
        }
        
        
        new_row.append(name_elem)
        new_row.append(is_instock)
        table_body.append(new_row)
    });
})