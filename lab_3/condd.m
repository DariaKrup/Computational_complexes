function [Cminim]=condd(A, infA, supA, b1, par)
Cminim = -1;
if par == 1
    for i1=inf(A(1,1)):(sup(A(1,1))-inf(A(1,1))):sup(A(1,1))
        for i2=inf(A(1,2)):(sup(A(1,2))-inf(A(1,2))):sup(A(1,2))
            for j1=inf(A(2,1)):(sup(A(2,1))-inf(A(2,1))):sup(A(2,1))
                for j2=inf(A(2,2)):(sup(A(2,2))-inf(A(2,2))):sup(A(2,2))
                    for k1=inf(A(3,1)):(sup(A(3,1))-inf(A(3,1))):sup(A(3,1))
                        for k2=inf(A(3,2)):(sup(A(3,2))-inf(A(3,2))):sup(A(3,2))
                            if cond([i1 i2;j1 j2;k1 k2])<=b1
                                Cminim=cond([i1 i2;j1 j2;k1 k2]);
                            end
                        end
                    end
                end
            end
        end
    end
end
if par == -1
    for i1=inf(A(1,1)):(sup(A(1,1))-inf(A(1,1))):sup(A(1,1))
        for i2=inf(A(1,2)):(sup(A(1,2))-inf(A(1,2))):sup(A(1,2))
            for i3=inf(A(1,3)):(sup(A(1,3))-inf(A(1,3))):sup(A(1,3))
                for j1=inf(A(2,1)):(sup(A(2,1))-inf(A(2,1))):sup(A(2,1))
                       for j2=inf(A(2,2)):(sup(A(2,2))-inf(A(2,2))):sup(A(2,2))
                            for j3=inf(A(2,3)):(sup(A(2,3))- inf(A(2,3))):sup(A(2,3))
                                if cond([i1 i2 i3;j1 j2 j3])<=b1
                                    Cminim=cond([i1 i2 i3;j1 j2 j3]);
                                end
                            end
                       end
                end
            end
        end
    end
end