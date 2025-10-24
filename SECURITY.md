# Security Guidelines

This document outlines security best practices and considerations for the Portfolio Management Application.

## Critical Security Considerations

### 1. API Keys and Secrets

#### OpenAI API Key
- **Never commit** API keys to version control
- Store in `.env` file (already in `.gitignore`)
- Use environment variables in production
- Rotate keys regularly
- Monitor API usage for anomalies

#### Database Credentials
- Change default passwords in production
- Use strong, randomly generated passwords
- Consider using secrets management:
  - AWS Secrets Manager
  - HashiCorp Vault
  - Azure Key Vault
  - Google Cloud Secret Manager

#### Flask Secret Key
- Generate a strong random secret key
- Never use the default development key in production
- Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

### 2. Network Security

#### Production Deployment
- **Always use HTTPS/TLS** for all endpoints
- Obtain SSL certificates (Let's Encrypt for free)
- Configure proper firewall rules
- Use private networks/VPCs when possible
- Implement rate limiting on API endpoints

#### Port Exposure
- Only expose necessary ports to the internet
- Use a reverse proxy (nginx, Caddy)
- Consider API gateway for additional security

### 3. Authentication & Authorization

#### Current State
- Application currently has **no authentication**
- All endpoints are publicly accessible

#### Recommended Additions
```python
# Add to requirements.txt
flask-jwt-extended==4.5.3
flask-login==0.6.3

# Implement user authentication
# Protect sensitive endpoints
# Add role-based access control (RBAC)
```

#### Example Implementation
```python
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

@app.route('/api/portfolios', methods=['POST'])
@jwt_required()
def create_portfolio():
    # Only authenticated users can create portfolios
    pass
```

### 4. Input Validation

#### Current Protections
- Basic validation on ticker symbols
- Type checking on numeric inputs

#### Recommendations
```python
# Add to requirements.txt
marshmallow==3.20.1

# Implement schema validation
from marshmallow import Schema, fields, validate

class HoldingSchema(Schema):
    ticker = fields.Str(required=True, validate=validate.Length(min=1, max=10))
    shares = fields.Float(required=True, validate=validate.Range(min=0.01))
    purchase_price = fields.Float(required=True, validate=validate.Range(min=0.01))
```

### 5. Database Security

#### Implemented Protections
- SQL injection protection via SQLAlchemy ORM
- Parameterized queries

#### Production Recommendations
- Enable PostgreSQL SSL/TLS
- Implement connection pooling with pgBouncer
- Regular database backups (encrypted)
- Enable PostgreSQL audit logging
- Use read replicas for sensitive data isolation

#### PostgreSQL SSL Configuration
```yaml
# docker-compose.yml
postgres:
  environment:
    POSTGRES_SSL_MODE: require
  volumes:
    - ./ssl/server.crt:/var/lib/postgresql/server.crt
    - ./ssl/server.key:/var/lib/postgresql/server.key
```

### 6. Data Protection

#### Sensitive Data
- Portfolio holdings and values
- User investment information
- API keys and credentials

#### Recommendations
- Encrypt data at rest (database encryption)
- Encrypt data in transit (HTTPS/TLS)
- Implement data retention policies
- Add audit logging for data access
- Consider PII (Personally Identifiable Information) handling

### 7. Dependency Security

#### Regular Updates
```bash
# Check for vulnerabilities
pip install safety
safety check -r backend/requirements.txt

# Update dependencies
pip install --upgrade -r backend/requirements.txt
```

#### Automated Scanning
- Enable Dependabot on GitHub
- Use Snyk or similar tools
- Regular security audits

### 8. Container Security

#### Best Practices
- Use official, minimal base images
- Regularly update base images
- Scan images for vulnerabilities
- Don't run containers as root
- Limit container resources

#### Docker Security Scanning
```bash
# Scan Docker image
docker scan portfolio-backend:latest

# Use Trivy
trivy image portfolio-backend:latest
```

### 9. Monitoring & Logging

#### Security Monitoring
- Log all authentication attempts
- Monitor unusual API access patterns
- Alert on suspicious activities
- Track failed requests
- Monitor resource usage

#### Example Logging Implementation
```python
import logging
from datetime import datetime

security_logger = logging.getLogger('security')

@app.before_request
def log_request():
    security_logger.info(f"{datetime.utcnow()} - {request.remote_addr} - {request.method} {request.path}")
```

### 10. Rate Limiting

#### Implementation
```python
# Add to requirements.txt
flask-limiter==3.5.0

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/portfolios', methods=['POST'])
@limiter.limit("10 per minute")
def create_portfolio():
    pass
```

### 11. CORS Configuration

#### Current State
- CORS enabled for all origins (development)

#### Production Configuration
```python
# Restrict CORS to specific origins
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### 12. Error Handling

#### Security Considerations
- Don't expose internal errors to clients
- Log detailed errors server-side
- Return generic error messages
- Avoid information disclosure

#### Example
```python
@app.errorhandler(500)
def internal_error(error):
    # Log detailed error
    logger.error(f"Internal error: {error}")
    # Return generic message
    return jsonify({'error': 'An error occurred'}), 500
```

## Security Checklist

### Before Production Deployment

- [ ] Change all default passwords
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Implement authentication
- [ ] Add rate limiting
- [ ] Restrict CORS origins
- [ ] Enable database SSL
- [ ] Set up secrets management
- [ ] Configure monitoring/alerting
- [ ] Enable audit logging
- [ ] Regular backup strategy
- [ ] Update all dependencies
- [ ] Scan for vulnerabilities
- [ ] Review error handling
- [ ] Document security procedures
- [ ] Set up incident response plan

### Regular Maintenance

- [ ] Weekly: Review access logs
- [ ] Weekly: Check for security alerts
- [ ] Monthly: Update dependencies
- [ ] Monthly: Review user access
- [ ] Quarterly: Security audit
- [ ] Quarterly: Penetration testing
- [ ] Yearly: Comprehensive security review

## Incident Response

### If Security Breach Occurs

1. **Isolate** affected systems immediately
2. **Document** the incident
3. **Notify** relevant parties
4. **Investigate** root cause
5. **Remediate** vulnerabilities
6. **Review** and improve security measures

### Emergency Contacts
- Security team: security@example.com
- On-call engineer: Available via PagerDuty

## Compliance Considerations

### Financial Data Regulations
- GDPR (if serving EU users)
- SOC 2 compliance for financial data
- PCI DSS (if handling payments)
- Local financial regulations

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/security.html)

## Reporting Security Issues

If you discover a security vulnerability:
1. **Do not** open a public issue
2. Email: security@example.com
3. Include detailed description
4. Allow time for fix before disclosure

Thank you for helping keep the application secure! 🔒
