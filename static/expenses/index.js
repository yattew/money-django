const search_input = document.querySelector("#search-input");
const expense_table = document.querySelector(".expense-table > table");
const page_num_element = document.querySelector("#page_num");
const prev_page = document.querySelector("#prev_page");
const next_page = document.querySelector("#next_page");
const curr_page_num = document.querySelector("#curr_page_num");
function update_table(search_querry = "",page_num = 1) {
    let body = expense_table.querySelector("tbody");
    body.innerHTML = "";
    curr_page_num.innerText = page_num;
    fetch(`/expense_search/${page_num}`, {
        body: JSON.stringify({ "search_querry": search_querry, }),
        method: "POST"
    })
        .then((res) => res.json())
        .then((data) => {
            let expenses = data["expenses"];
            for (let r of expenses) {
                let row = document.createElement("tr");

                for (let c in r) {
                    if (c != "id") {
                        let col = document.createElement("td");
                        col.innerText = r[c];
                        row.appendChild(col);
                    }
                }
                let col = document.createElement("td");
                let edit_btn = document.createElement("a");
                edit_btn.innerText = "edit";
                edit_btn.href = `/edit_expense/${r["id"]}`;
                col.appendChild(edit_btn);
                row.appendChild(col);
                body.appendChild(row);
            }
            page_num_element.innerText = `showing ${data["curr_page"]} of ${data["tot_pages"]}`;
            if (data["curr_page"] == 1) {
                prev_page.style.display = "none";
                next_page.style.display = "inline";
            }
            else if (data["curr_page"] == data["tot_pages"]) {
                prev_page.style.display = "inline";
                next_page.style.display = "none";
            }
            else {
                prev_page.style.display = "inline";
                next_page.style.display = "inline";
            }
        });


};
update_table();



//even listeners
search_input.addEventListener('keyup', (e) => {
    const search_val = e.target.value;
    update_table(search_val.trim());
});

prev_page.addEventListener("click",()=>{
    // console.log(Number(curr_page_num.innerText)-1);
    update_table(search_input.value.trim(),Number(curr_page_num.innerText)-1);
});
next_page.addEventListener("click",()=>{
    // console.log(Number(curr_page_num.innerText)+1);
    update_table(search_input.value.trim(),Number(curr_page_num.innerText)+1);
});