import React, { useState, useRef, useEffect, useLayoutEffect } from "react";
import attachmentSvg from '../assets/attachment.svg';
import sendSvg from '../assets/send.svg';
import removeSvg from '../assets/remove.svg';


const ChatWindow = ({ chat, messages, sendMessage }) => {
  const [text, setText] = useState("");
  const [files, setFiles] = useState([]);
  const messagesEndRef = useRef(null);
  const textbox = useRef(null);
  const fileInput = useRef(null);

  // Автоматическая прокрутка вниз
  useEffect(() => {
    scrollToBottom();
  }, [messages]);


  function adjustHeight() {
    textbox.current.style.height = "inherit";
    let scrollHeight = textbox.current.scrollHeight
    if (textbox.current.scrollHeight > 200) { 
        scrollHeight = 200
    }
    textbox.current.style.height = `${scrollHeight}px`;
  }

  useLayoutEffect(adjustHeight, [text]);

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  const removeFile = (file) => {
    setFiles((prev) => prev.filter(function(existFile) {return existFile !== file}));
  }

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles((prev) => [...prev, ...selectedFiles]); // Оставляем максимум 10 файлов
  };

  const shiftEnterNewLine = async (event) => {
    const keyCode = event.which || event.keyCode;
    if (keyCode === 13 && !event.shiftKey) {
        event.preventDefault();
        handleSendMessage(event);
    }
  }

  const handleSendMessage = async (event) => {
    event.preventDefault();
    const attachmentIds = [];

    for (const file of files) {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/api_v1/attachment/file", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        attachmentIds.push(data.id);
      }
    }

    const messageData = {
      chat_id: chat.id,
      text,
      telegram_message_id: Date.now(),
      is_admin: true,
      attachments_ids: attachmentIds,
    };

    sendMessage(chat.id, messageData);

    // Очистка полей
    setText("");
    setFiles([]);
    fileInput.current.value = ""
  };

  return (
    <div className="chat-window">
      <div className="messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={message.is_admin ? "admin" : "user"}
          >
            <p>{message.text}</p>
            {message.attachments &&
              message.attachments.map((attachment) => (
                <a
                  key={attachment.id}
                  href={`/api_v1/attachment/file/${attachment.id}`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {attachment.filename}
                </a>
              ))}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="file-list">
            {files.map((file, index) => (
            <div key={index} className="file">
                <p>{file.name} ({(file.size / 1024).toFixed(1)} KB)</p>
                <div className="remove-file" onClick={(e) => removeFile(file)}><img src={removeSvg} alt="remove file" /></div>
            </div>
            ))}
        </div>
      <form className="message-input" onSubmit={handleSendMessage}>
        
        <textarea
          ref={textbox}
          type="textarea"
          value={text}
          onKeyDown={shiftEnterNewLine}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type a message"
          maxLength="4096"
        />
        <div className="message-action-container">
            <label htmlFor="file-upload" className="file-upload-label">
                <img className="custom-file-upload" src={attachmentSvg} alt="Add files" />
            </label>
            <input
            ref={fileInput}
            type="file"
            multiple
            id="file-upload"
            onChange={handleFileChange}
            />
            <button type="submit"><img src={sendSvg} alt="Send"/></button>
        </div>
      </form>
    </div>
  );
};

export default ChatWindow;
