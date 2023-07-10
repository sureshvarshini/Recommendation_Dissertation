import { createAuthProvider } from 'react-token-auth'
import axios from 'axios'

export const { useAuth, authFetch, login, logout } = createAuthProvider({
    accessTokenKey: 'access_token',
    onUpdateToken: token =>
        axios.post('/user/token/refresh', token.refresh_token)
            .then(flaskResponse => console.log(flaskResponse))
})