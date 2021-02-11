function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)
%NNCOSTFUNCTION Implements the neural network cost function for a two layer
%neural network which performs classification
%   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
%   X, y, lambda) computes the cost and gradient of the neural network. The
%   parameters for the neural network are "unrolled" into the vector
%   nn_params and need to be converted back into the weight matrices. 
% 
%   The returned parameter grad should be a "unrolled" vector of the
%   partial derivatives of the neural network.
%

% Reshape nn_params back into the parameters ThetactLayer1 and ThetactLayer2, the weight matrices
% for our 2 layer neural network
ThetactLayer1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

ThetactLayer2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

% Setup some useful variables
m = size(X, 1);
         
% You need to return the following variables correctly 
J = 0;
ThetactLayer1_grad = zeros(size(ThetactLayer1));
ThetactLayer2_grad = zeros(size(ThetactLayer2));

% ====================== YOUR CODE HERE ======================
% Instructions: You should complete the code by working through the
%               following parts.
%
% Part 1: Feedforward the neural network and return the cost in the
%         variable J. After implementing Part 1, you can verify that your
%         cost function computation is correct by verifying the cost
%         computed in ex4.m
%
% Part 2: Implement the backpropagation algorithm to compute the gradients
%         ThetactLayer1_grad and ThetactLayer2_grad. You should return the partial derivatives of
%         the cost function with respect to ThetactLayer1 and ThetactLayer2 in ThetactLayer1_grad and
%         ThetactLayer2_grad, respectively. After implementing Part 2, you can check
%         that your implementation is correct by running checkNNGradients
%
%         Note: The vector y passed into the function is a vector of labels
%               containing values from 1..K. You need to map this vector into a 
%               binary vector of 1's and 0's to be used with the neural network
%               cost function.
%
%         Hint: We recommend implementing backpropagation using a for-loop
%               over the training examples if you are implementing it for the 
%               first time.
%
% Part 3: Implement regularization with the cost function and gradients.
%
%         Hint: You can implement this around the code for
%               backpropagation. That is, you can compute the gradients for
%               the regularization separately and then add them to ThetactLayer1_grad
%               and ThetactLayer2_grad from Part 2.
%

                    %ThetactLayer1 = 25x401
                    %ThetactLayer2 = 10x26

gradL1 = 0;
gradL2 = 0;

for i=1:m
    actLayer1 = [1 X(i,:)];
    
    zValLayer2 = actLayer1 * ThetactLayer1';
    actLayer2 = [1 sigmoid(zValLayer2)];
    
    zValLayer3 = actLayer2 * ThetactLayer2';
    actLayer3 = sigmoid(zValLayer3);
    
    yReshaped = zeros(num_labels, 1);
    yReshaped(y(i)) = 1;
    
    J = J + (-yReshaped' * log(actLayer3') - ... 
      (1 - yReshaped') * log(1 - actLayer3'));
    J = J + lambda / (2 * m) * ...
      (sum(sum(ThetactLayer1(:,2:end).^2)) + sum(sum(ThetactLayer2(:,2:end).^2)));
    
    deltactLayer3 = actLayer3' - yReshaped;
    deltactLayer2 = ThetactLayer2' * deltactLayer3 .* sigmoidGradient([1 zValLayer2])';
    gradL1 = gradL1 + deltactLayer2(2:end) * actLayer1;
    gradL2 = gradL2 + deltactLayer3 * actLayer2;
end

J = J / m;

ThetactLayer1_grad = 1 / m * gradL1;
ThetactLayer2_grad = 1 / m * gradL2;

nonBiasedThetactLayer1 = ThetactLayer1;
nonBiasedThetactLayer1(:,1) = 0;
ThetactLayer1_grad = ThetactLayer1_grad + lambda / m * nonBiasedThetactLayer1;

nonBiasedThetactLayer2 = ThetactLayer2;
nonBiasedThetactLayer2(:,1) = 0;
ThetactLayer2_grad = ThetactLayer2_grad + lambda / m * nonBiasedThetactLayer2;                    
                    
                    
##X = [ones(m, 1) X]; %5000x401
##
##Calculation for z values of hidden layer
##zVal1 = X*ThetactLayer1'; %5000x25
##
##Calculation for activation value of hidden layers
##hiddenLayer = sigmoid(zVal1); 
##hiddenLayer = [ones(m, 1) hiddenLayer]; %5000x26
##
##Calculation for z values of output layer
##zVal2 = hiddenLayer*ThetactLayer2'; %5000x10
##
##Calculation for activation values of output layer
##outputLayer = sigmoid(zVal2); %5000x10
##
##Creating Reshaped Version of Matrix y
##yReshaped = zeros(m, size(outputLayer, 2));
##
##for i = 1:m
##  yReshaped(i, y(i)) = 1; %5000x10
##end
##
##Solving for Cost Value
##lenThetactLayer1 = size(ThetactLayer1, 2)
##lenThetactLayer2 = size(ThetactLayer2, 2)
##
##J = (1/m)*sum(sum(((-yReshaped).*(log(outputLayer)) ...
##  -(1-yReshaped).*(log(1-outputLayer))), 2), 1) ...
##  + (lambda/(2*m))*((sum(sum(ThetactLayer1(:, 2:lenThetactLayer1).^2, 2), 1)) ...
##  + (sum(sum(ThetactLayer2(:, 2:lenThetactLayer2).^2, 2), 1)));
##
##Backpropagation
##gradL1 = 0
##gradL2 = 0
##
##for t = 1:m
##  gradL2 = X(t, :); %1x401
##  
##  zValLayer2 = (ThetactLayer1*gradL2')'; %1x25
##  actLayer2 = sigmoid(zValLayer2); 
##  actLayer2 = [1 actLayer2]; %1x26
##  
##  actLayer2 = (ThetactLayer2*actLayer2')'; %1x10
##  actLayer3 = sigmoid(actLayer2); %1x10
##  
##  yReshaped = zeros(num_labels, 1);
##  yReshaped(y(i)) = 1;
##  
##  J = J+(-yReshaped')
##  
##  grad3 = (actLayer3 - yReshaped(t, :)); %1x10
##  
##  grad2 = (ThetactLayer2'*grad3')(2:end) ... %26x1 -> 25x1
##    .*sigmoidGradient(zValLayer2'); %25x1
##    
##  gradL1 = gradL1+(grad2*gradL2); %25x401
##  gradL2 = gradL2+(grad3'*actLayer2); %10x26
##end
  
  
##%Backpropagation
##for t = 1:m
##  fprintf("Iteration number: ") 
##  t
##  
##  %Important Matrices for Gradient Calculation for ThetactLayer2
##  outputLayerTrain = outputLayer(t, :)';
##  yTrain = yReshaped(t, :)';
##  zVal2Train = zVal2(t, :)';
##  
##  for i = 1:(size(ThetactLayer2, 2)-1)
##    outputLayerTrain = [outputLayerTrain outputLayer(t, :)']; %10x26
##    yTrain = [yTrain yReshaped(t, :)']; %10x26
##    zVal2Train = [zVal2Train zVal2(t, :)']; %10x26
##  end
##  
##  hidLayerTrain = hiddenLayer(t, :);
##  
##  for i = 1:size(outputLayer, 2)-1
##    hidLayerTrain = [hidLayerTrain; hiddenLayer(t, :)]; %10x26
##  end
##  
##  %Calculation for Gradient of ThetactLayer2
##  ThetactLayer2_grad = 2*(outputLayerTrain - yTrain) ... 
##    .*((sigmoid(zVal2Train)).*(1-sigmoid(zVal2Train))) ...
##    .*(hidLayerTrain);
##  
##  %Calculation for Gradient of ThetactLayer1
##  ijMatrix = zeros(size(ThetactLayer1_grad, 1), size(outputLayer, 2)); %25x10
##  hiMatrix = zeros(size(ThetactLayer1_grad, 2), size(ThetactLayer1_grad, 1)); %401x25
##  
##  for h = 1:size(ThetactLayer1_grad, 2)
##    for i = 1:size(ThetactLayer1_grad, 1)
##      for j = 1:size(outputLayer, 2)
##        ijMatrix(i, j) = 2*(outputLayer(t, j)-yReshaped(t, j)) ...
##          .*((sigmoid(zVal2(t, j))).*(1-sigmoid(zVal2(t, j)))) ...
##          .*(ThetactLayer2'(i+1, j));
##        
##      end
##      
##      hiMatrix(h, i) = sum(ijMatrix(i, :), 2)' ...
##        .*((sigmoid(zVal1(t, i))).*(1-sigmoid(zVal1(t, i)))) ...
##        *X(t, h);
##    end
##  end
##  
##  ThetactLayer1_grad = hiMatrix;
##  
##end









% -------------------------------------------------------------

% =========================================================================

% Unroll gradients
grad = [ThetactLayer1_grad(:) ; ThetactLayer2_grad(:)];


end
