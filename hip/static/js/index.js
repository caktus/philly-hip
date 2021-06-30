import JQuery from "jquery";
/**
 * Javascript files must be imported here.
 * Webpack uses this file as the entry-point for bundling.
 */


 /** Sentry Init
  *
  * This import, if you choose to use sentry logging for javascript, should stay at the top of this file.
  *
 */
// import '../../../apps/home/static/js/sentryInit';

/** App imports
  *
  * Import javascript for your apps here
  *
 */

import Common from "./common";
import Header from "../../../apps/hip/static/js/header";
import SideBar from "../../../apps/hip/static/js/sidebar";
import RightScrollNav from "../../../apps/hip/static/js/rightScrollNav";
import MobileSearchModal from "../../../apps/hip/static/js/mobileSearchModal";
import LoggedInDropdown from "../../../apps/hip/static/js/loggedInDropdown";
import HealthAlertFilter from "../../../apps/health_alerts/static/js/healthAlertFilter";
import HealthAlertMessage from "../../../apps/health_alerts/static/js/healthAlertMessage";
import NotificationSignup from "../../../apps/notifications/static/js/notificationSignup";
import ContactInformationEditModal from "../../../apps/auth_content/static/js/contactInformationEdit";

document.addEventListener("DOMContentLoaded", function() {
  Common();
  Header();
  SideBar();
  MobileSearchModal();
  LoggedInDropdown();
  RightScrollNav();
  HealthAlertFilter();
  HealthAlertMessage();
  NotificationSignup();
  ContactInformationEditModal();
});
