import { MdAccountCircle, MdSettings, MdOutlineChat } from 'react-icons/md';

function ToolBar(){

  return (
    <>
      <div className="tool-bar">
        <button className="profile-button">
          <MdAccountCircle className='profile-icon' size={50}></MdAccountCircle>
        </button>

        <button className="settings-button">
          <MdSettings className="settings-icon" size={50}></MdSettings>
        </button>
      </div>
    </>
  );
}

export default ToolBar