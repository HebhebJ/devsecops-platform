package com.devsecops.auth.services.interfaces;

import com.devsecops.auth.dto.LoginRequest;
import com.devsecops.auth.dto.MeResponse;
import com.devsecops.auth.dto.RegisterRequest;
import com.devsecops.auth.dto.TokenResponse;

public interface AuthService {
    void register(RegisterRequest request);

    TokenResponse login(LoginRequest request);

    MeResponse me(String username);
}
