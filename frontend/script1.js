const API_URL = "http://127.0.0.1:8000";


// ==============================
// Upload PDF
// ==============================

document.getElementById("uploadBtn").addEventListener("click", async () => {

    const fileInput = document.getElementById("pdfFile");
    const status = document.getElementById("uploadStatus");

    if (!fileInput.files.length) {
        status.textContent = "Please choose a PDF first.";
        return;
    }

    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);

    status.textContent = "Uploading PDF...";

    try {

        const response = await fetch(`${API_URL}/upload`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        status.textContent = data.message;

    } catch (error) {

        status.textContent = "Upload failed.";

        console.error(error);
    }

});


// ==============================
// Ask Question
// ==============================

document.getElementById("askBtn").addEventListener("click", async () => {

    const questionInput = document.getElementById("question");
    const answerElement = document.getElementById("answer");
    const sourceElement = document.getElementById("source");

    const question = questionInput.value.trim();


    // Check question

    if (!question) {

        answerElement.textContent =
            "Please enter a question.";

        return;
    }


    // Show loading

    answerElement.textContent =
        "🤔 Thinking...";

    sourceElement.textContent =
        "Searching your document...";


    try {

        const response = await fetch(
            `${API_URL}/ask?query=${encodeURIComponent(question)}`
        );

        const data = await response.json();


        // Show AI answer

        answerElement.textContent =
            data.answer;


        // Show source

        const sources = data.sources
            .map(item => item.source)
            .filter(
                (value, index, array) =>
                    array.indexOf(value) === index
            );


        sourceElement.textContent =
            sources.join(", ");


        // Clear question box

        questionInput.value = "";


    } catch (error) {

        answerElement.textContent =
            "❌ Something went wrong. Please check whether the backend is running.";

        sourceElement.textContent = "";

        console.error(error);
    }

});