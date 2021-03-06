const search_input = document.querySelector("#search-input");
const expense_table = document.querySelector(".expense-table > table");
const page_num_element = document.querySelector("#page_num");
const prev_page = document.querySelector("#prev_page");
const next_page = document.querySelector("#next_page");
const curr_page_num = document.querySelector("#curr_page_num");


function update_table(search_querry = "", page_num = 1) {
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
            if (data["curr_page"] == data["tot_pages"] && data["curr_page"] == 1) {
                prev_page.style.display = "none";
                next_page.style.display = "none";
            }
            else if (data["curr_page"] == data["tot_pages"]) {
                prev_page.style.display = "inline";
                next_page.style.display = "none";
            }
            else if (data["curr_page"] == 1) {
                prev_page.style.display = "none";
                next_page.style.display = "inline";
            }
            else {
                prev_page.style.display = "inline";
                next_page.style.display = "inline";
            }
        });


};

function plot_pie_chart(labels, values) {
    const ctx = document.getElementById('pie-chart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: "Expenditure in last 30 days on different categories",
                    position: "top",
                    font: {
                        size: 17
                    }
                },
                legend: {
                    position: "right",
                    maxHeight: 1,
                    labels: {
                        font: {
                            size: 15
                        }
                    }
                }
            },

        },
    });
}

function plot_line_chart(labels,values) {
    const ctx = document.getElementById('line-chart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                ],
                fill: false,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: "Expenditure in last 30 days",
                    position: "top",
                    font: {
                        size: 17
                    }
                },
                legend: {
                    display: false,
                }
            },

        },
    });
}


function plot_charts() {
    fetch("expense_summary")
        .then((res) => res.json())
        .then((data) => {
            const [pie_data, line_data] = [data["pie_data"], data["line_data"]];
            const [p_labels, p_values] = [
                Object.keys(pie_data), Object.values(pie_data)
            ];
            const [l_labels, l_values] = [
                Object.keys(line_data), Object.values(line_data)
            ];
            plot_pie_chart(p_labels, p_values);
            plot_line_chart(l_labels,l_values);
        });
}
function main() {
    update_table();
    plot_charts();
    //even listeners
    search_input.addEventListener('keyup', (e) => {
        const search_val = e.target.value;
        update_table(search_val.trim());
    });

    prev_page.addEventListener("click", () => {
        // console.log(Number(curr_page_num.innerText)-1);
        update_table(search_input.value.trim(), Number(curr_page_num.innerText) - 1);
    });
    next_page.addEventListener("click", () => {
        // console.log(Number(curr_page_num.innerText)+1);
        update_table(search_input.value.trim(), Number(curr_page_num.innerText) + 1);
    });
}

main();

