import Cookies from "js-cookie";
import {jwtDecode} from "jwt-decode"; 
// 需要安装jwt-decode库，npm install jwt-decode

function checkAuthorizaion() {
    const token = Cookies.get("token");
    if (token) {
        try {
            const decodedToken = jwtDecode(token);
            const currentTime = Date.now() / 1000;
            if (decodedToken.exp > currentTime) {
                sessionStorage.setItem("token", token);
                return true;
            } else {
                return false;
            }
        } catch (error) {
            console.error("Token解析失败:", error);
            return false;
        }
    } else {
        return false;
    }
}

function logout() {
    Cookies.remove("token");
    sessionStorage.removeItem("token");
}
export { checkAuthorizaion, logout };