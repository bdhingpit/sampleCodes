function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta

lenTheta = length(theta);
lenX = length(X(1,:));

size(y')
size((log(sigmoid(theta'(1,1)*X'(1,:))))')

    
J = (1/m)*((-y)'*(log(sigmoid(theta'*X')))' ...
    - (1-y)'*(log(1-sigmoid(theta'*X')))') ...
    + (lambda/(2*m))*sum(theta(2:lenTheta,1).^2);

grad(1,1) = ((1/m)*(sigmoid(theta'*X')-y')*X(:,1))';

%sigmoid = 1x118, sigmoid - y' = 1x118, (sigmoid - y')*X = 1x118*118x1 = 1x1

grad(2:lenTheta,1) = (1/m)*((sigmoid(theta'*X')-y')*X(:,2:lenX))' ...
    + (lambda/m)*theta(2:lenTheta,1);

%sigmoid = 1x118, sigmoid - y' = 1x118, (sigmoid - y')*X = 1x118*118x27 = 1x27
% =============================================================

end
