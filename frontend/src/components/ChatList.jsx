import React, { useState } from "react";

const ChatList = ({ chats, lastMessages, onSelectChat, selectedChat }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const filteredChats = chats.filter((chat) => {
    const query = parseInt(searchQuery, 10); // Преобразуем строку в число
      return isNaN(query) || chat.telegram_id === query; // Фильтруем по telegram_id
  });
  return (
    <div className="chat-list">
      <h3>Telegram support</h3>
      <input
        type="text"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Search chats..."
        className="search-input"
      />
      <div className="chats">
        {filteredChats.map((chat) => (
          <div 
            className={"chat " + (chat.is_read ? "" : "unread ") + (chat?.id === selectedChat?.id? "active" : "") }
            key={chat.id}
            onClick={() => onSelectChat(chat)}
          >
            <p className="telegram_id">{chat.first_name} ({chat.telegram_id})</p>
            <p className="last_message">{lastMessages[chat.id]}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChatList;
