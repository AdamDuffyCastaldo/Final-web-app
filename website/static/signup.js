const form = document.querySelector("form"),
  firstnamefield = form.querySelector(".firstname-field"),
  firstname_input = firstnamefield.querySelector(".firstname"),
  Lastnamefield = form.querySelector(".LastName"),
  Lastname_input = Lastnamefield.querySelector(".Lastname-input"),
  Passkeyfield = form.querySelector(".createPasskey"),
  Passkeyinput = Passkeyfield.querySelector(".inputpasskey"),
  Cpassfield = form.querySelector(".ConfirmPassKey"),
  Cpassinput = Cpassfield.querySelector(".Confirminput");

function checkPassKey() {
  const passkeypattern =
    /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{7,}$/;
  if (!Passkeyinput.value.match(passkeypattern)) {
    return Passkeyfield.classList.add("invalid"); // adding invalid class if passkey value do not match pattern
  }
  Passkeyfield.classList.remove("invalid");
}

function ConfirmPassKey() {
  if (Passkeyinput.value !== Cpassinput.value || Cpassinput.value === "") {
    return Cpassfield.classList.add("invalid");
  }
  Cpassfield.classList.remove("invalid");
}

function AllLetters() {
  const letters = /^[A-Za-z\s]+$/;
  if (!firstname_input.value.match(letters)) {
    firstnamefield.classList.add("invalid");
    return false;
  }
  firstnamefield.classList.remove("invalid");
  return true;
}

function AllLettersL() {
  const letters = /^[A-Za-z\s]+$/;
  if (!Lastname_input.value.match(letters)) {
    Lastnamefield.classList.add("invalid");
    return false;
  }
  Lastnamefield.classList.remove("invalid");
  return true;
}

const eyeIcons = document.querySelectorAll(".show-PassKey");

eyeIcons.forEach((eyeIcon) => {
  eyeIcon.addEventListener("click", () => {
    const pInput = eyeIcon.parentElement.querySelector("input"); // getting parent element and selecting the input
    if (pInput.type === "password") {
      eyeIcon.classList.replace("bx-hide", "bx-show");
      return (pInput.type = "text");
    }
    eyeIcon.classList.replace("bx-show", "bx-hide");
    pInput.type = "password";
  });
});

function CheckBoth() {
  a = AllLettersL();
  b = AllLetters();
  return a && b;
}
const button = document.querySelector(".Next");

let pagenumber = 1;

button.addEventListener("click", (e) => {
  e.preventDefault();

  //prevents form submitting
  checkPassKey();
  ConfirmPassKey();
  AllLetters();
  AllLettersL();

  //Passkeyinput.addEventListener("keyup", checkPassKey);
  firstname_input.addEventListener("keyup", CheckBoth);
  Lastname_input.addEventListener("keyup", CheckBoth);
  Passkeyinput.addEventListener("keyup", checkPassKey);
  Cpassinput.addEventListener("keyup", ConfirmPassKey);

  if (!CheckBoth()) {
    return;
  }
  //Cpassinput.addEventListener("keyup", ConfirmPassKey)
  pagenumber += 1;
  if (pagenumber > 1) {
    document.querySelector(".prev").removeAttribute("disabled");
    document.querySelector(".Next").setAttribute("disabled", "");
  }
  document.querySelector("#Camera").classList = ["Stage3"];
  document.querySelector("#Confirm").classList = ["Stage4"];
  document.querySelector("#pass").classList = ["Stage2 hidden"];
  document.querySelector("#Names").classList = ["Stage1 hidden"];
  //document.querySelector("#EnterNames").classList = ["input-field hidden"];
});

const previousbutton = document.querySelector(".prev");

previousbutton.addEventListener("click", (e) => {
  document.querySelector("#Camera").classList = ["Stage3 hidden"];
  document.querySelector("#Confirm").classList = ["Stage4 hidden"];
  document.querySelector("#pass").classList = ["Stage2"];
  document.querySelector("#Names").classList = ["Stage1"];

  pagenumber -= 1;
  if (pagenumber === 1) {
    previousbutton.setAttribute("disabled", "");
    document.querySelector(".Next").removeAttribute("disabled");
  }
});

const videoElement = document.getElementById("videoElement");
const canvasElement = document.getElementById("canvaselement");
const photoelement = document.getElementById("photoelement");
const startButton = document.getElementById("startcamera");
const capturebutton = document.getElementById("takephoto");

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
  formData.append('firstname', firstname_input.value);
  formData.append('lastname', Lastname_input.value);
  formData.append('passkey', Passkeyinput.value);
  formData.append('cPasskey', Cpassinput.value);
  formData.append('image', imageData);

  // Send a POST request to the server
  try {
    const response = await fetch('/signup', {
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
const submitbutton = document.getElementById("Submitform")
// Modify button click event listener to call sendData function
submitbutton.addEventListener('click', (e) => {
  e.preventDefault();
  // Call function to send data
  sendData();
});