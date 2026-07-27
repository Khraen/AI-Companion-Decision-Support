import ChatBar from "./ChatBar"
import ToolBar from "./ToolBar"
import MessageBoxContainer from "./MessageBoxContainer";
import {useState, useEffect} from 'react'
function App() {
  // holds chat log of current conversation
  const [chat_log, setChatLog] = useState([ //dummy data to start
                                            { id: 1, text: "Hello! How can I help you today?", sender: "Cortana" },
                                            { id: 2, text: "Howdy!", sender: "User" }
                                          ]);


  const [isLoading, setIsLoading] = useState(false)
// holds profile.json content
  const [profile, setProfile] = useState(null);
  //holds summary.json content
  const [summary, setSummary] = useState(null);
  // holds list of messages. (last 14 back n forths)
  const [context, setContext] = useState([]);

  // holds profile/summary data view
  const [activeView, setActiveView] = useState("profile");


//Get engine state from api and update UI on mount
  useEffect(()=>{
    fetch("http://localhost:8000/api/Get-Engine-State").then((response) => response.json())
    .then((data) =>{
      setProfile(data.profile);
      setSummary(data.summary);
      setContext(data.context);

      console.log("set profile, summary, context on app mount");
    
    }).catch((error) =>{
    console.log("Error retrieving engine state from server:", error.message);

    })
  },[])

  // Handle Memory Consolidation on closed connections
  useEffect(() => {
    const handleUnloading = ()=>{
      fetch("http://localhost:8000/api/Consolidate-Memory", {
        method: "PUT",
        keepalive: true
      })
    }
    window.addEventListener("beforeunload",handleUnloading)
    return () => {
      window.removeEventListener("beforeunload", handleUnloading)
    }
  },)


  const handleMessage = async (user_message) => {
    const user_msg_obj = {id:Date.now(), text: user_message, sender: "User"};

    setChatLog(prevChatLogs =>[...prevChatLogs, user_msg_obj ]);

    //display waiting indicator for the user when waiting for the api.

    setIsLoading(true);
    try{
      const response = await fetch("http://localhost:8000/api/Process-User-Message",
      {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({"message":user_message})
      }
    );
    const data = await response.json();

    //append ai message
    const ai_response_obj = {id:Date.now()+1, text:data.response_message, sender: "Cortana"};
    setChatLog((prevChatLogs) => [...prevChatLogs, ai_response_obj]);
    console.log("Cortana's response is:", data.response_message);
    }
    catch(error){
      console.error("Error sending message to the Engine:", error);
    }
    finally{
      // turn the waiting indicator off to show there is nothing left the wait for.
      setIsLoading(false);
    }
  }

  function ChangeActiveViewProfile(){
    setActiveView("profile")
  }
  function ChangeActiveViewSummary(){
    setActiveView("summary")
  }


  return (
    <>
    <div className="app-layout">
      <ToolBar></ToolBar>
      <div className="content-area">
        <div className="image-placeholder">image</div>
        <MessageBoxContainer messages={chat_log} isLoading={isLoading}></MessageBoxContainer>
        <ChatBar sendMessage = {handleMessage}></ChatBar>
      </div>
      <div className="input-area">
        <h1 className="input-area-title" id="view-area-title">
          {activeView === "profile" ? "Profile" : "Summary"}
        </h1>
          <div className="profile-view" id="profile-summary-panel"> 
                {activeView === "profile" ? (
              profile ? (
                <pre style={{ 
                  fontSize: '11px', 
                  textAlign: 'left', 
                  whiteSpace: 'pre-wrap', 
                  wordBreak: 'break-word',
                  margin: 0 
                }}>
                  {JSON.stringify(profile, null, 2)}
                </pre>
              ) : (
                <p>Loading profile...</p>
              )
            ) : (
              summary ? (
                <pre style={{ 
                  fontSize: '11px', 
                  textAlign: 'left', 
                  whiteSpace: 'pre-wrap', 
                  wordBreak: 'break-word',
                  margin: 0 
                }}>
                  {JSON.stringify(summary, null, 2)}
                </pre>
              ) : (
                <p>Loading summary...</p>
              )
            )}
           </div>
        
      
        <div className="profile-summary-btn-container">
            <button className="view-profile-button" id="profile-view-button" onClick={ChangeActiveViewProfile}>View Profile</button>
            <button className="view-summary-button" id="summary-view-button" onClick={ChangeActiveViewSummary}>View Summary</button>
        </div>
      </div>
    </div>
    
    
    </>

  )
}

export default App
