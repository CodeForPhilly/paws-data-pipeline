import { useContext } from "react";
import AlertContext from "../contexts/AlertContext";

const useAlert = () => useContext(AlertContext);

export default useAlert;
