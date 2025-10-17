export class ChatManager {
  constructor(apiManager, app) {
    this.apiManager = apiManager;
    this.app = app;
    this.chatContainer = document.getElementById("chatMessages");
    this.messageInput = document.getElementById("messageInput");
    this.sendButton = document.getElementById("sendButton");
    this.typingIndicator = null;
    this.setupEventListeners();
  }

  setupEventListeners() {
    this.sendButton.addEventListener("click", () => this.sendMessage());
    this.messageInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });
    document.querySelectorAll(".quick-action").forEach((button) => {
      button.addEventListener("click", () => {
        this.messageInput.value = button.textContent.trim();
        this.sendMessage();
      });
    });
  }

  async sendMessage() {
    const messageText = this.messageInput.value.trim();
    if (!messageText) return;

    this.messageInput.value = "";
    this.addMessage(messageText, "user");
    this.showTypingIndicator();

    try {
      const response = await this.apiManager.getChatResponse(
        messageText,
        this.app.getCurrentCity()
      );
      this.hideTypingIndicator();
      this.addMessage(response, "ai");
    } catch (error) {
      this.hideTypingIndicator();
      this.addMessage("⚠️ Failed to get response. Please try again.", "system");
    }
  }

  addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className =
      sender === "user"
        ? "bg-primary text-white p-3 rounded-lg max-w-xs ml-auto shadow"
        : sender === "ai"
        ? "bg-gray-100 text-gray-900 p-3 rounded-lg max-w-xs shadow"
        : "bg-red-100 text-red-700 p-3 rounded-lg max-w-xs mx-auto text-center shadow";
    msg.innerHTML = text.replace(/\n/g, "<br>"); // Basic markdown for newlines
    this.chatContainer.appendChild(msg);
    this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
  }

  showTypingIndicator() {
    if (this.typingIndicator) return;
    this.typingIndicator = document.createElement("div");
    this.typingIndicator.className =
      "bg-gray-200 text-gray-600 italic p-2 rounded-lg max-w-xs shadow";
    this.typingIndicator.textContent = "Typing...";
    this.chatContainer.appendChild(this.typingIndicator);
    this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
  }

  hideTypingIndicator() {
    if (this.typingIndicator) {
      this.typingIndicator.remove();
      this.typingIndicator = null;
    }
  }

  clearMessages() {
    this.chatContainer.innerHTML = "";
  }

  sendWelcomeMessage(city) {
    this.addMessage(`Welcome to ${city}! How can I help you today?`, "ai");
  }
}
