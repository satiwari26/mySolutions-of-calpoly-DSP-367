function xn = append_zeros(xn,num_z)
% Given a time-domain function, x[n], append zeros to it
%   

% set length of DFT equal to length of signal
N = length(xn);

for i = N+1:N+num_z
     xn(i) = 0;
end

return

end

