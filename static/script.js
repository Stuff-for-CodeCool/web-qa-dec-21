const link = document.querySelector("a");
const resultContainer = document.querySelector("#result");

const loadData = async (e) => {
    e.preventDefault();
    resultContainer.innerHTML = "Please wait...";

    const request = await fetch(e.target.href, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    });
    if (request.ok) {
        const response = await request.json();
        console.log(response);

        resultContainer.innerHTML = JSON.stringify(response, null, 4);
    }
};

link.addEventListener("click", loadData);
