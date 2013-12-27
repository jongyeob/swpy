'''
Created on 2013. 4. 16.

@author: kasi
'''

import scipy.linalg


#____________________  Support functions _______________________
# calculate Euclidean distance between two points p and q and
# return the distance as a scalar:
def _euclidean(p, q):
    p,q = scipy.array(p), scipy.array(q)
    return scipy.sqrt( scipy.dot(p-q,p-q) )

# calculate Euclidean distance from a point p to the list of
# points in data and return a list of all such distances
def _dist(p, data):
    return [_euclidean(p,q) for q in data]

def _indexAndLeastDistance(distList):
    minVal = min(distList)
    return distList.index(minVal), minVal    

def _difference(p,q):
    return p[0]-q[0],p[1]-q[1]

def _mean_coordinates(coords_list):
    '''
    Returns a pair of values in the form of a tuple, the pair
    consisting of the mean values for the x and the y coordinates.
    '''
    mean = reduce(lambda x,y: x+y, [x[0] for x in coords_list]), \
           reduce(lambda x,y: x+y, [x[1] for x in coords_list])
    mean = mean[0]/float(len(coords_list)), mean[1]/float(len(coords_list))
    return mean


def calculate(model_list,data_list,iterations=100,error_threshold=1):

    ## Initialize ##
    R = scipy.matrix( [[1.0, 0.0],[0.0, 1.0]] )
    T = (scipy.matrix([[0.0, 0.0]])).T
    
    ## Swapping data and model when the number of data is less then its model.
    
#    if len(data_list) > len(model_list):
#        print ">>>> SWAPPING THE MODEL AND THE DATA IMAGES <<<<\n\n"
#        data_list, model_list = model_list, data_list        
        
    '''
    Since two patterns that are situated at different places in a 
    plane may not be related by a Euclidean transform for an 
    arbitrary placement of the origin even when one pattern appears to 
    be a rotated version of the other, we will assume that the origin 
    for ICP calculations will be at the "center" of the model image.  
    Now our goal becomes to find an R and a T that will make the data 
    pattern congruent with the model pattern with respect to this 
    origin.
    '''
        
    # Need to do the following separately because we calculate 
    # model mean from only the sparse set for color images
    model_mean = (scipy.matrix(list(_mean_coordinates(model_list)))).T
    zero_mean_model_list = [(p[0] - model_mean[0,0], p[1] - model_mean[1,0]) for p in model_list]
    zero_mean_data_list = [(p[0] - model_mean[0,0], p[1] - model_mean[1,0]) for p in data_list]
    
    print "model mean:\n", model_mean
    print "zero mean model list: ", zero_mean_model_list
    print "zero mean data list: ", zero_mean_data_list
    print "\n\n"
    
    
    '''
    In the plane whose origin is at the model center, the relationship
    between the model points x_m and the data points x_d is given by
         R . x_d  +  T  =  x_m
    Let the list of the n chosen data points be given by
         A =  [x_d1, x_d2, .....,   x_dn]
    We can now express the relationship between the data and the 
    model points by
         R . A  = B
    where B is the list of the CORRESPONDING model points after 
    we subtract the translation form each:
         B =  [x_m1 - T, x_m2 - T, ......,  x_mn - T] 
    Eventually our goal will be to estimate R from the R.A = B 
    relationship.
    '''
     
    A = scipy.matrix( [ [p[0] for p in zero_mean_data_list], [p[1] for p in zero_mean_data_list] ] )

    
    '''
    So we want to estimate R from R.A = B.  If we had to construct a 
    one-shot estimate for R (note ICP is iterative and not one-shot),
    we would write R.A=B as 
             R.A.A^t  =  B.A^t
    and then
             R =  B . A^t . (A . A^t)^-1
    We will group together what comes after B on the right hand side
    and write
             AATI  =  A^t . (A . A^t)^-1
    In the ICP implementation, this matrix will remain the same for all
    the iterations.
    '''
    
    AATI = A.T * scipy.linalg.inv( A * A.T )
    
    old_error = float('inf')
    iteration = 0
    
    model = zero_mean_model_list
    data = zero_mean_data_list
    
 
    while 1:
        print "\n>>>>>>>>>>   STARTING ITERATION ", iteration, " OUT OF ", iterations, "\n"
        if iteration >= iterations: break

        data_matrix = [ R * (scipy.matrix( list(data[p]) )).T + T \
                                            for p in range(len(data)) ] 
        data_transformed = [ ( p[0,0], p[1,0] ) for p in data_matrix]

        # For every data point find the closest model point.  The set of such
        # model points will be called the matched_model set of points
        # The following returns a list of pairs, the first the index of 
        # the model point that was found closest to the data point in question,
        # and the second the actual minimal distance
        leastDistMapping = [_indexAndLeastDistance(_dist(p,model)) for p in data_transformed]
        
        #matched_model = [model[p[0]] for p in leastDistMapping]
        matched_index = []
        matched_model = []
        for p in leastDistMapping:
            matched_model.append(model[p[0]])
            matched_index.append(p[0])
            
        matched_model_mean = scipy.matrix(list(_mean_coordinates(matched_model))).T
        error = reduce(lambda x, y: x + y, [x[1] for x in leastDistMapping])
        error = error / len(leastDistMapping)
        print "old_error: ", old_error, "    error: ", error
        print "\n"
        diff_error = abs(old_error - error)
        if (diff_error > error_threshold):
            old_error = error
        else:
            iterations = iteration
            break
        
        B = scipy.matrix([ [p[0] - T[0,0] for p in matched_model], \
                           [p[1] - T[1,0] for p in matched_model] ])
        
        R_update = B * AATI * R.T
        [U,S,VT] = scipy.linalg.svd(R_update)
        U,VT = scipy.matrix(U), scipy.matrix(VT) 
        deter = scipy.linalg.det(U * VT)
        U[0,1] = U[0,1] * deter
        U[1,1] = U[1,1] * deter
        R_update = U * VT
        R = R_update * R
        print "Rotation:\n", R
        print "\n"
        # Rotate the data for estimating the translation T
        data_matrix2 = [ R * (scipy.matrix( list(data[p]))).T  \
                                            for p in range(len(data)) ] 
        data_transformed2 = [ ( p[0,0], p[1,0] ) for p in data_matrix2]
        data_transformed_mean = \
              scipy.matrix(list(_mean_coordinates(data_transformed2))).T
        T = matched_model_mean - data_transformed_mean  
        print "Translation:\n", T
        print "\n"
        # Now apply the R,T transformation to the original data for updated image
        # representation of the result at the end of this iteration

        data_matrix_new = [ R * (scipy.matrix( list(data[p]))).T + T for p in range(len(data)) ] 
        data_transformed_new = [ ( p[0,0] + model_mean[0,0], p[1,0] + model_mean[1,0] ) for p in data_matrix_new]
        
        iteration = iteration + 1
        
    return matched_index, data_transformed_new