import React, { useState, useEffect } from "react";
import ChatList from "./ChatList";
import ChatWindow from "./ChatWindow";
import useWebSocket from "../hooks/useWebSocket";

const ChatApp = () => {
  const [lastMessages, setLastMessages] = useState({});
  const [selectedChat, setSelectedChat] = useState(null);
  const [chats, setChats] = useState([]);
  const [messages, setMessages] = useState({});
  const { sendMessage } = useWebSocket(setChats, setMessages, setLastMessages);

  useEffect(() => {
    // Select chat by url param
    if (!selectedChat && chats.length) {
        const queryParameters = new URLSearchParams(window.location.search)
        const queryChatId = queryParameters.get("chat");
        setSelectedChat(chats.find(chat => chat.id === queryChatId));
    }
  }, [chats]);

  useEffect(() => {
    if (selectedChat) {
      // Set url param by selected chat
      const nextURL = `?chat=${selectedChat.id}`;
      const nextTitle = 'Chat';
      const nextState = { additionalInformation: 'Selected chat' };
      window.history.pushState(nextState, nextTitle, nextURL);
      window.history.replaceState(nextState, nextTitle, nextURL);
    }
  }, [selectedChat]);

  return (
    <div className="chat-app">
      <div className="left-panel">
        <ChatList 
          chats={chats} 
          lastMessages={lastMessages} 
          onSelectChat={(chat) => setSelectedChat(chat)} 
          selectedChat={selectedChat} 
        />
      </div>
      <div className="right-panel">
        {selectedChat ? (
          <ChatWindow
            chat={selectedChat}
            messages={messages[selectedChat.id] || []}
            sendMessage={sendMessage}
          />
        ) : (
          <div className="placeholder">Select a chat to start messaging</div>
        )}
      </div>
    </div>
  );
};

export default ChatApp;
