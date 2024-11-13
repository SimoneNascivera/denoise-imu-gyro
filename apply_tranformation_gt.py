import csv
import numpy as np
from scipy.spatial.transform import Rotation as R  # Add this import

def quaternion_to_rotation_matrix(q):
    # Convert quaternion from [w, x, y, z] to [x, y, z, w]
    q_scipy = [q[1], q[2], q[3], q[0]]
    r = R.from_quat(q_scipy)
    return r.as_matrix()

def rotation_matrix_to_quaternion(R_mat):
    r = R.from_matrix(R_mat)
    q_scipy = r.as_quat()
    # Convert quaternion from [x, y, z, w] to [w, x, y, z]
    q = [q_scipy[3], q_scipy[0], q_scipy[1], q_scipy[2]]
    return q

# Define the homogeneous transformation matrix T
T = np.eye(4)  # Replace with your transformation matrix
T[:3, :3] = quaternion_to_rotation_matrix(np.array([0.62321, 0.234, 0.8543, 0.87654]))  # Replace with your rotation matrix

with open('data/EUROC/MH_03_medium/mav0/state_groundtruth_estimate0/data.csv', 'r') as infile, open('out.csv', 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Read and write header
    header = next(reader)
    writer.writerow(header)

    for row in reader:
        # Parse timestamp, position, and quaternion
        timestamp = row[0]
        p_RS_R = np.array(row[1:4], dtype=float)
        q_RS = np.array(row[4:8], dtype=float)

        # Convert position to homogeneous coordinates
        p_hom = np.append(p_RS_R, 1)

        # Apply transformation to position
        p_transformed_hom = T @ p_hom
        p_transformed = p_transformed_hom[:3]

        # Convert quaternion to rotation matrix
        R_mat = quaternion_to_rotation_matrix(q_RS)

        # Apply transformation to rotation matrix
        R_transformed = T[:3, :3] @ R_mat

        # Convert back to quaternion
        q_transformed = rotation_matrix_to_quaternion(R_transformed)

        # Write transformed data
        writer.writerow([timestamp] + list(p_transformed) + list(q_transformed))
