import { ReactComponent as RedHatLogo } from '../../assets/redhat.svg';
import "./Header.scss";

function Header() {
  return (
    <div id="header-container">
            <div>
                <RedHatLogo id="red-hat-logo"/>
            </div>

            <p id="diary-title"> | My Diary</p>

    </div>
  );
}
export default Header;