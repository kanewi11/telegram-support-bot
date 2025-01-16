import { useEffect, useRef, useCallback } from "react";

const useWebSocket = (setChats, setMessages, setLastMessages) => {
  const chatSockets = useRef({});
  const mainSocket = useRef(null);
  const updateInterval = useRef(null);

  const initializeChatSocket = useCallback((chatId) => {
    if (chatSockets.current[chatId] && chatSockets.current[chatId].readyState === WebSocket.OPEN) return;

    const chatSocket = new WebSocket(`ws://localhost:8000/api_v1/chats/ws/${chatId}`);

    chatSocket.onmessage = (event) => {
      try {
        const chatData = JSON.parse(event.data);

        if (Array.isArray(chatData)) {
          const chatMessages = chatData.map((message) => JSON.parse(message));
          setMessages((prev) => ({
            ...prev,
            [chatId]: chatMessages,
          }));
          setLastMessages((prev) => ({
            ...prev,
            [chatId]: chatMessages.at(-1)?.text || "",
          }));
        } else {
          setMessages((prev) => ({
            ...prev,
            [chatId]: [...(prev[chatId] || []), chatData],
          }));
          setLastMessages((prev) => ({
            ...prev,
            [chatId]: chatData.text,
          }));
        }
      } catch (error) {
        console.error("Error parsing chat messages:", error);
      }
    };

    chatSocket.onclose = () => {
      console.log(`Chat WebSocket for chat ${chatId} closed`);
      delete chatSockets.current[chatId];
    };

    chatSockets.current[chatId] = chatSocket;
  }, [setMessages, setLastMessages]);

  useEffect(() => {
    // Initialize main WebSocket
    mainSocket.current = new WebSocket("ws://localhost:8000/api_v1/chats/ws");

    mainSocket.current.onopen = () => {
      console.log("Main WebSocket connection established");
      mainSocket.current.send("update");

      // Start sending "update" every second
      updateInterval.current = setInterval(() => {
        if (mainSocket.current?.readyState === WebSocket.OPEN) {
          mainSocket.current.send("update");
        }
      }, 2000);
    };

    mainSocket.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (Array.isArray(data)) {
          const chats = data.map((chat) => JSON.parse(chat));
          setChats(chats);

          chats.forEach((chat) => {
            initializeChatSocket(chat.id);
          });
        }
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    mainSocket.current.onclose = () => {
      console.log("Main WebSocket connection closed");
      if (updateInterval.current) {
        clearInterval(updateInterval.current);
        updateInterval.current = null;
      }
    };

    return () => {
      // Cleanup: close main socket and all chat sockets
      if (mainSocket.current) {
        mainSocket.current.close();
      }
      Object.values(chatSockets.current).forEach((socket) => socket.close());
      chatSockets.current = {};

      if (updateInterval.current) {
        clearInterval(updateInterval.current);
        updateInterval.current = null;
      }
    };
  }, [initializeChatSocket, setChats]);

  const sendMessage = useCallback((chatId, messageData) => {
    const chatSocket = chatSockets.current[chatId];
    if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
      chatSocket.send(JSON.stringify(messageData));
    } else {
      console.error(`WebSocket for chat ${chatId} is not open or does not exist`);
    }
  }, []);

  return { sendMessage };
};

export default useWebSocket;
