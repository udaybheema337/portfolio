(function(){
  // Theme toggle
  const root = document.documentElement;
  const themeBtn = document.getElementById("themeToggle");
  const saved = localStorage.getItem("theme");
  if(saved) root.setAttribute("data-theme", saved);
  themeBtn.textContent = root.getAttribute("data-theme")==="light" ? "☀️" : "🌙";
  themeBtn.addEventListener("click", () => {
    const cur = root.getAttribute("data-theme")==="light" ? "dark" : "light";
    root.setAttribute("data-theme", cur);
    localStorage.setItem("theme", cur);
    themeBtn.textContent = cur==="light" ? "☀️" : "🌙";
  });

  // Hire button
  const hireBtn = document.getElementById("hireButton");
  if(hireBtn) hireBtn.addEventListener("click", ()=> location.href="#contact");

  // Tracking helper
  function sendTrack(action){
    try{
      const payload = { action, platform: navigator.platform || "", browser: navigator.userAgent || "" };
      fetch("/track", { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(payload) }).catch(()=>{});
    }catch(e){}
  }
  sendTrack("view");

  // resume hooks
  const resumeBtn = document.getElementById("downloadResume");
  if(resumeBtn) resumeBtn.addEventListener("click", ()=> sendTrack("download_resume"));



  // Project tiles: hover play & click open modal
  const projects = document.querySelectorAll('.project');
  const modal = document.getElementById('videoModal');
  const modalVideo = document.getElementById('modalVideo');
  const modalTitle = document.getElementById('modalTitle');
  const modalClose = document.getElementById('modalClose');

  projects.forEach(proj => {
    const vid = proj.querySelector('video');
    // hover play
    proj.addEventListener('mouseenter', ()=> { if(vid) vid.play().catch(()=>{}); });
    proj.addEventListener('mouseleave', ()=> { if(vid){ vid.pause(); vid.currentTime=0; } });

    // click to open modal
    proj.addEventListener('click', (e)=>{
      const src = proj.dataset.video;
      const title = proj.dataset.title || "";
      if(!src) return;
      modal.classList.add('show');
      modalVideo.src = src;
      modalVideo.play().catch(()=>{});
      modalTitle.textContent = title;
      sendTrack("open_project");
    });
  });

  // modal close
  if(modalClose){
    modalClose.addEventListener('click', ()=> {
      modal.classList.remove('show');
      modalVideo.pause();
      modalVideo.currentTime = 0;
      modalVideo.src = "";
    });
  }
  // close on backdrop click
  modal.addEventListener('click', (e)=>{
    if(e.target === modal){
      modal.classList.remove('show');
      modalVideo.pause();
      modalVideo.currentTime = 0;
      modalVideo.src = "";
    }
  });
  const typedEl = document.getElementById("typed");

if (typedEl) {
  const phrases = JSON.parse(typedEl.dataset.text);
  let i = 0, j = 0, forward = true;

  setInterval(() => {
    const text = phrases[i];

    if (forward) {
      j++;
      if (j === text.length) forward = false;
    } else {
      j--;
      if (j === 0) {
        forward = true;
        i = (i + 1) % phrases.length;
      }
    }

    typedEl.textContent = text.slice(0, j);
  }, 80);
}
    // HIRE ME BUTTON — SMOOTH SCROLL TO CONTACT
    document.addEventListener("DOMContentLoaded", () => {
        const hireBtn = document.getElementById("hireButton");
        if (hireBtn) {
            hireBtn.addEventListener("click", () => {
                const contactSection = document.querySelector("#contact");
                if (contactSection) {
                    contactSection.scrollIntoView({ behavior: "smooth" });
                }
            });
        }
    });

      // Certificate Image Modal
    document.addEventListener("DOMContentLoaded", () => {
      const certModal = document.getElementById("certModal");
      const certModalImg = document.getElementById("certModalImg");
      const certClose = document.getElementById("certClose");

      document.querySelectorAll(".cert-open").forEach(img => {
        img.addEventListener("click", () => {
          certModal.style.display = "block";
          certModalImg.src = img.dataset.full; // Load full image
        });
      });

      certClose.addEventListener("click", () => certModal.style.display = "none");

      certModal.addEventListener("click", (e) => {
        if (e.target === certModal) certModal.style.display = "none";
      });
    });


  // Chat
    const chatLog = document.getElementById("chatLog");
    const chatForm = document.getElementById("chatForm");
    const chatInput = document.getElementById("chatInput");

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const text = chatInput.value.trim();
        if (!text) return;

        // USER BUBBLE
        chatLog.insertAdjacentHTML(
            "beforeend",
            `<div class="msg-user">${text}</div>`
        );
        chatInput.value = "";

        // Scroll down
        chatLog.scrollTop = chatLog.scrollHeight;

        // Send to backend
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        const data = await res.json();
        const reply = data.reply || "I didn't understand that.";

        // BOT BUBBLE
        chatLog.insertAdjacentHTML(
            "beforeend",
            `<div class="msg-bot">${reply}</div>`
        );

        // Scroll down
        chatLog.scrollTop = chatLog.scrollHeight;
    });

  // Toggle Chatbot Window
const chatToggle = document.getElementById("chatToggle");
const chatWindow = document.getElementById("chatWindow");
const closeChat = document.getElementById("closeChat");

chatToggle.onclick = () => {
    chatWindow.style.display = "flex";
    chatToggle.style.display = "none";
};

closeChat.onclick = () => {
    chatWindow.style.display = "none";
    chatToggle.style.display = "flex";
};


})();
