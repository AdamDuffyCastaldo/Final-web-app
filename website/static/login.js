const videoElement = document.getElementById("videoElement");
const canvasElement = document.getElementById("canvaselement");
const photoelement = document.getElementById("photoelement");
const startButton = document.getElementById("startcamera");
const capturebutton = document.getElementById("takephoto");
const firstname = document.getElementById("login__firstname");
const lastname = document.getElementById("login_lastname");
const password = document.getElementById("Passkey");

let stream;

async function startWebcam() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoElement.srcObject = stream;
    startButton.disabled = true;
    capturebutton.disabled = false;
  } catch (error) {
    console.error("Error accessing webcam", error);
  }
}

startButton.addEventListener("click", function (event) {

  event.preventDefault();

  startWebcam();
});

let isExecuted = false;

function capturepicture() {
  isExecuted = true;
  canvasElement.width = videoElement.videoWidth;
  canvasElement.height = videoElement.videoHeight;
  canvasElement.getContext("2d").drawImage(videoElement, 0, 0);
  const photodataurl = canvasElement.toDataURL("image/png");
  photoelement.src = photodataurl;
  photoelement.style.display = "block";
}

capturebutton.addEventListener("click", function (event) {
  event.preventDefault();
  capturepicture();
});

function dataURLtoBlob(dataURL) {
  var arr = dataURL.split(","),
    mime = arr[0].match(/:(.*?);/)[1],
    bstr = atob(arr[1]),
    n = bstr.length,
    u8arr = new Uint8Array(n);

  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }

  return new Blob([u8arr], { type: mime });
}

// Function to send form data and image to the server
async function sendData() {
  // Convert canvas image to binary format
  const canvasDataUrl = canvasElement.toDataURL("image/png");
  const imageData = dataURLtoBlob(canvasDataUrl);
  
  let imageName = photoelement.src ? "image.png" : "empty.png";
  // Create a FormData object and append form data
  const formData = new FormData();
  formData.append("firstname", firstname.value);
  formData.append("lastname", lastname.value);
  formData.append("image", imageData, imageName);

  const passwordValue = password.value.trim();
  if (passwordValue) {
    formData.append("password", passwordValue);
  }


  try {
    const response = await fetch("/login", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      console.log("Data sent successfully");
      const responseData = await response.json();
      const issamepredict = responseData.issamepredict;
      if (issamepredict) {
        window.location.href = "/";
        console.log("Faces are the same");
      } else {
        window.location.reload();
        // Handle login failure with issamepredict
        console.log("Faces are different or invalid credentials");
      }
    } else {

      const errorMessage = await response.text();
      console.error("HTTP Error:", errorMessage);
    }
  } catch (error) {

    console.error("Network Error:", error);
  }
}

const submitbutton = document.getElementById("login_submit");

submitbutton.addEventListener("click", async (e) => {
  e.preventDefault();
  await sendData();
});
