from hackathon_backend.schemas.role import RoleName

# Polities example
role_policies_map = {
    RoleName.ADMINISTRADOR.value: {
        "/roles": ["GET", "POST", "PUT", "DELETE"],
        "/users": ["GET", "POST", "PUT", "DELETE"],
        "/clinics": ["GET", "POST"],
        "/": ["GET"],
    },
    RoleName.DOCTOR.value: {
        "/me": ["GET", "PUT"],
        "/": ["GET"],
    },
    RoleName.PATIENT.value: {
        "/me": ["GET", "PUT"],
        "/": ["GET"],
    },
    RoleName.CLINIC_ADMINISTRATOR.value: {
        "/clinics": ["GET", "POST"],
        "/users": ["GET", "POST"],
        "/": ["GET"],
    },
}

# Generate the policies
policies = [
    (role, path, method)
    for role, endpoints in role_policies_map.items()
    for path, methods in endpoints.items()
    for method in methods
]
