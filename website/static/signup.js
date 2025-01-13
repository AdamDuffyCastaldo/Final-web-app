document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector("form");
  const firstnamefield = form.querySelector(".firstname-field");
  const firstname_input = firstnamefield.querySelector(".firstname");
  const Lastnamefield = form.querySelector(".LastName");
  const Lastname_input = Lastnamefield.querySelector(".Lastname-input");
  const Passkeyfield = form.querySelector(".createPasskey");
  const Passkeyinput = Passkeyfield.querySelector(".inputpasskey");
  const Cpassfield = form.querySelector(".ConfirmPassKey");
  const Cpassinput = Cpassfield.querySelector(".Confirminput");

  function checkPassKey() {
    const passkeypattern =
      /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{7,}$/;
    if (!Passkeyinput.value.match(passkeypattern)) {
      Passkeyfield.classList.add("invalid");
      return false;
    }
    Passkeyfield.classList.remove("invalid");
    return true;
  }

  function ConfirmPassKey() {
    if (Passkeyinput.value !== Cpassinput.value || Cpassinput.value === "") {
      Cpassfield.classList.add("invalid");
      return false;
    }
    Cpassfield.classList.remove("invalid");
    return true;
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
      const pInput = eyeIcon.parentElement.querySelector("input");
      if (pInput.type === "password") {
        eyeIcon.classList.replace("bx-hide", "bx-show");
        return (pInput.type = "text");
      }
      eyeIcon.classList.replace("bx-show", "bx-hide");
      pInput.type = "password";
    });
  });

  function CheckBoth() {
    const a = AllLettersL();
    const b = AllLetters();
    return a && b;
  }
  function CheckBothPasswords() {
    const a = checkPassKey();
    const b = ConfirmPassKey();
    return a && b;
  }


  firstname_input.addEventListener("keyup", CheckBoth);
  Lastname_input.addEventListener("keyup", CheckBoth);
  Passkeyinput.addEventListener("keyup", checkPassKey);
  Cpassinput.addEventListener("keyup", ConfirmPassKey);

  const button = document.querySelector(".Next");
  let pagenumber = 1;

  button.addEventListener("click", (e) => {
    e.preventDefault();

    if (!CheckBoth() || !CheckBothPasswords()) {
      pagenumber = 1;
      return;
    }

    pagenumber += 1;
    if (pagenumber > 1) {
      document.querySelector(".prev").removeAttribute("disabled");
      document.querySelector(".Next").setAttribute("disabled", "");
    }
    document.querySelector("#Camera").classList = ["Stage3"];
    document.querySelector("#Confirm").classList = ["Stage4"];
    document.querySelector("#pass").classList = ["Stage2 hidden"];
    document.querySelector("#Names").classList = ["Stage1 hidden"];
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
    event.preventDefault();
    startWebcam();
  });

  function capturepicture() {
    canvasElement.width = videoElement.videoWidth;
    canvasElement.height = videoElement.videoHeight;
    canvasElement.getContext("2d").drawImage(videoElement, 0, 0);
    const photodataurl = canvasElement.toDataURL("image/png");
    if (!photodataurl || photodataurl === 'data:,') {
      console.error('Please capture an image before submitting the form.');
      window.location.reload(); // Reload the page
      return;
    }
    photoelement.src = photodataurl;
    photoelement.style.display = "block";
  }

  capturebutton.addEventListener("click", function(event) {
    event.preventDefault();
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

  async function sendData() {
    const canvasDataUrl = canvasElement.toDataURL('image/png');
    
    // Check if canvas is empty
    const context = canvasElement.getContext("2d");
    const imageData = context.getImageData(0, 0, canvasElement.width, canvasElement.height);
    const isEmpty = !Array.from(imageData.data).some(channel => channel !== 0);
    
    const formData = new FormData();
    formData.append('firstname', firstname_input.value);
    formData.append('lastname', Lastname_input.value);
    formData.append('passkey', Passkeyinput.value);
    formData.append('cPasskey', Cpassinput.value);
  

    if (!isEmpty) {
      const blob = dataURLtoBlob(canvasDataUrl);
      formData.append('image', blob, 'image.png');
    } else {

      formData.append('image', 'empty.png');
    }
  
    try {
      const response = await fetch('/signup', {
        method: 'POST',
        body: formData
      });
  
      if (response.ok) {
        const responseData = await response.json();
        const isAccountCreated = responseData.isAccountCreated;
        if (isAccountCreated) {
          console.log('Account created successfully');
          window.location.href = '/'; // Redirect to home page
        } else {
          console.error('Account creation failed');
         
          location.reload();
        }
      } else {
        console.error('Failed to create account');
        
        location.reload();
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
  const submitbutton = document.getElementById('Submitform');
  submitbutton.addEventListener('click', async (e) => {
    e.preventDefault();
    await sendData();
  });
});
