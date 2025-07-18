# AWS Deployment Guide for TravelAiGent

## Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI installed and configured
3. Docker installed locally
4. Environment variables ready

## Deployment Options

### Option 1: AWS Elastic Beanstalk (Recommended for Quick Deploy)

1. **Install EB CLI**:
   ```bash
   pip install awsebcli
   ```

2. **Initialize Elastic Beanstalk**:
   ```bash
   eb init -p docker travelaigent
   ```

3. **Create environment**:
   ```bash
   eb create travelaigent-prod
   ```

4. **Set environment variables**:
   ```bash
   eb setenv SECRET_KEY=your-secret-key \
     AMADEUS_CLIENT_ID=your-amadeus-id \
     AMADEUS_CLIENT_SECRET=your-amadeus-secret \
     OPENAI_API_KEY=your-openai-key \
     ADMIN_USERNAME=admin \
     ADMIN_PASSWORD=your-secure-password
   ```

5. **Deploy**:
   ```bash
   eb deploy
   ```

### Option 2: AWS ECS with Fargate

1. **Build and push Docker image to ECR**:
   ```bash
   # Create ECR repository
   aws ecr create-repository --repository-name travelaigent
   
   # Get login token
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [your-account-id].dkr.ecr.us-east-1.amazonaws.com
   
   # Build image
   docker build -t travelaigent .
   
   # Tag image
   docker tag travelaigent:latest [your-account-id].dkr.ecr.us-east-1.amazonaws.com/travelaigent:latest
   
   # Push image
   docker push [your-account-id].dkr.ecr.us-east-1.amazonaws.com/travelaigent:latest
   ```

2. **Create ECS Task Definition** (save as `task-definition.json`):
   ```json
   {
     "family": "travelaigent",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "512",
     "memory": "1024",
     "containerDefinitions": [
       {
         "name": "travelaigent",
         "image": "[your-account-id].dkr.ecr.us-east-1.amazonaws.com/travelaigent:latest",
         "portMappings": [
           {
             "containerPort": 8000,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {"name": "FLASK_ENV", "value": "production"}
         ],
         "secrets": [
           {"name": "SECRET_KEY", "valueFrom": "arn:aws:secretsmanager:region:account:secret:travelaigent/secret-key"},
           {"name": "AMADEUS_CLIENT_ID", "valueFrom": "arn:aws:secretsmanager:region:account:secret:travelaigent/amadeus-id"},
           {"name": "AMADEUS_CLIENT_SECRET", "valueFrom": "arn:aws:secretsmanager:region:account:secret:travelaigent/amadeus-secret"},
           {"name": "OPENAI_API_KEY", "valueFrom": "arn:aws:secretsmanager:region:account:secret:travelaigent/openai-key"}
         ],
         "logConfiguration": {
           "logDriver": "awslogs",
           "options": {
             "awslogs-group": "/ecs/travelaigent",
             "awslogs-region": "us-east-1",
             "awslogs-stream-prefix": "ecs"
           }
         }
       }
     ]
   }
   ```

3. **Create ECS Service**:
   ```bash
   # Register task definition
   aws ecs register-task-definition --cli-input-json file://task-definition.json
   
   # Create cluster
   aws ecs create-cluster --cluster-name travelaigent-cluster
   
   # Create service
   aws ecs create-service \
     --cluster travelaigent-cluster \
     --service-name travelaigent-service \
     --task-definition travelaigent:1 \
     --desired-count 2 \
     --launch-type FARGATE \
     --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
   ```

### Option 3: AWS EC2 Instance

1. **Launch EC2 instance** (Amazon Linux 2 or Ubuntu)
2. **SSH into instance and install Docker**:
   ```bash
   sudo yum update -y
   sudo yum install docker -y
   sudo service docker start
   sudo usermod -a -G docker ec2-user
   ```

3. **Clone repository**:
   ```bash
   git clone https://github.com/your-repo/travelaigent.git
   cd travelaigent
   ```

4. **Create .env file** with your credentials
5. **Run with docker-compose**:
   ```bash
   docker-compose up -d
   ```

## Database Considerations

### For Production:

1. **Use AWS RDS PostgreSQL**:
   - Create RDS instance
   - Update DATABASE_URL to PostgreSQL connection string
   - Run migrations

2. **Use AWS DynamoDB** (requires code changes):
   - Create DynamoDB tables
   - Update models to use boto3

## Load Balancing & SSL

1. **Application Load Balancer (ALB)**:
   - Create ALB
   - Configure target groups
   - Add SSL certificate from ACM

2. **CloudFront Distribution** (optional):
   - For global performance
   - Additional caching layer

## Monitoring

1. **CloudWatch Logs**:
   - All logs automatically sent to CloudWatch
   - Set up alarms for errors

2. **CloudWatch Metrics**:
   - Monitor CPU, memory, request count
   - Set up auto-scaling policies

## Security Best Practices

1. **AWS Secrets Manager**:
   - Store all sensitive environment variables
   - Rotate secrets regularly

2. **Security Groups**:
   - Only allow necessary ports (443 for HTTPS)
   - Restrict SSH access

3. **IAM Roles**:
   - Use roles instead of access keys
   - Principle of least privilege

## Cost Optimization

1. **Elastic Beanstalk**: ~$50-100/month for small instance
2. **ECS Fargate**: ~$30-50/month for minimal setup
3. **EC2**: ~$10-30/month for t3.micro/small

## Deployment Commands Summary

```bash
# Quick deploy to Elastic Beanstalk
eb init -p docker travelaigent
eb create travelaigent-prod
eb setenv [environment variables]
eb deploy

# View logs
eb logs

# Open application
eb open
```

## Post-Deployment

1. Test all functionality
2. Set up monitoring alerts
3. Configure backup strategy
4. Update DNS records
5. Enable CloudWatch alarms

## Troubleshooting

1. **Database Connection Issues**:
   - Check security group rules
   - Verify DATABASE_URL format

2. **Memory Issues**:
   - Increase container memory
   - Check for memory leaks

3. **API Rate Limits**:
   - Implement caching
   - Use Redis for session storage