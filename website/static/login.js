const videoElement = document.getElementById("videoElement");
const canvasElement = document.getElementById("canvaselement");
const photoelement = document.getElementById("photoelement");
const startButton = document.getElementById("startcamera");
const capturebutton = document.getElementById("takephoto");
const firstname = document.getElementById("login__firstname");
const lastname = document.getElementById("login_lastname");

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
startButton.addEventListener("click", function(event) {
  // Prevent the default form submission behavior
  event.preventDefault();
  // Call the startWebcam function
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
capturebutton.addEventListener("click", function(event) {
  // Prevent the default form submission behavior
  event.preventDefault();
  // Call the startWebcam function
  capturepicture();
});

function dataURLtoBlob(dataURL) {
    var arr = dataURL.split(','), 
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), 
        n = bstr.length, 
        u8arr = new Uint8Array(n);
        
    while(n--){
      u8arr[n] = bstr.charCodeAt(n);
    }
    
    return new Blob([u8arr], {type:mime});
  }
  
  // Function to send form data and image to the server
  async function sendData() {
    // Convert canvas image to binary format
    const canvasDataUrl = canvasElement.toDataURL('image/png');
    const imageData = dataURLtoBlob(canvasDataUrl);
  
    // Create a FormData object and append form data
    const formData = new FormData();
    formData.append('firstname', firstname.value);
    formData.append('lastname', lastname.value);
    formData.append('image', imageData);
  
    // Send a POST request to the server
    try {
      const response = await fetch('/login', {
        method: 'POST',
        body: formData
      });
  
      if (response.ok) {
        // Handle success response
        console.log('Data sent successfully');
      } else {
        // Handle error response
        console.error('Error sending data');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
  const submitbutton = document.getElementById("login_submit")
  // Modify button click event listener to call sendData function
  submitbutton.addEventListener('click', (e) => {
    e.preventDefault();
    // Call function to send data
    sendData();
  });