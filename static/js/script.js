document.getElementById("file-input").addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById("preview").src = e.target.result;
            document.getElementById("preview").style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById("upload-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const fileInput = document.getElementById("file-input");
    if (!fileInput.files.length) {
        alert("Please select an image!");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch("http://127.0.0.1:8000/predict/", {  // 🔥 FIXED URL
            method: "POST",
            body: formData
        });

        const result = await response.json();
        document.getElementById("result").innerText = 
            `Prediction: ${result.predicted_class} (Confidence: ${(result.confidence * 100).toFixed(2)}%)`;
    } catch (error) {
        document.getElementById("result").innerText = "Error processing the image.";
    }
});
