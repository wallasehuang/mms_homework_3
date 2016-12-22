import image_retrieval_q1 as q1
import image_retrieval_q2 as q2
import image_retrieval_q3 as q3
import image_retrieval_q4 as q4


# generate color_histogram.csv
q1.color_histogram('dataset')

# generate color_layout.csv
q2.color_layout('dataset')

# generate sift.csv
q3.img_to_sift('dataset','dataset_sift')
q3.img_to_vector('dataset_sift')

# generate sift_stop_word_list.csv
q4.create_stop_word_list()
q4.create_vector_stop_word_list('dataset_sift')

