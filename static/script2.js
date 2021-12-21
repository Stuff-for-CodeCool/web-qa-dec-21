const results = document.querySelector("#result");
const form = document.querySelector("form");

const handleSubmit = async (e) => {
    e.preventDefault();

    results.innerHTML = "<p>Please wait...</p>";

    const req = await fetch(form.action, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: form.name.value,
            email: form.email.value,
        }),
    });

    if (req.ok) {
        const res = await req.json();
        results.innerHTML = `<p>Hello, ${res.name}, your email is ${res.email}</p>`
    }
};

form.addEventListener("submit", handleSubmit);
