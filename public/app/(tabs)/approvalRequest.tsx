import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  Image,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator
} from 'react-native';

export default function ApprovalPage() {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [relation, setRelation] = useState('');

  useEffect(() => {
    if (!processing) {
      fetchImage();
    }
  }, [processing]);

  const fetchImage = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/get-new-images');

      if (response.status === 204) {
        setTimeout(fetchImage, 5000); // No image available, retry after 5 seconds
        return;
      }

      if (!response.ok) {
        throw new Error('Failed to fetch image');
      }

      const data = await response.json();
      if (data.image_url) {
        setImageUrl(data.image_url);
        setLoading(false);
        setProcessing(true);  // Pause fetching until approval/denial is completed
      } else {
        setTimeout(fetchImage, 5000); // Retry if no image available
      }
    } catch (error) {
      console.error('Error fetching image:', error);
      setTimeout(fetchImage, 5000); // Retry fetching after failure
    }
  };

  const handleApprove = async () => {
    if (!name.trim() || !description.trim() || !relation.trim()) {
      Alert.alert('Error', 'Please fill in all fields before approving.');
      return;
    }

    if (!imageUrl) return;

    try {
      setProcessing(true);
      const response = await fetch('http://localhost:5000/api/approve', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: 'approve', name, description, relation, imageUrl }),
      });

      if (!response.ok) throw new Error('Failed to submit approval');

      Alert.alert('Success', 'The image has been approved.');
      resetForm();
    } catch (error) {
      Alert.alert('Error', 'Failed to submit approval');
    }
  };

  const handleDeny = async () => {
    if (!imageUrl) return;

    try {
      setProcessing(true);
      const response = await fetch('http://localhost:5000/api/deny', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: 'deny' }),
      });

      if (!response.ok) throw new Error('Failed to deny image');

      Alert.alert('Denied', 'The image has been denied.');
      resetForm();
    } catch (error) {
      Alert.alert('Error', 'Failed to deny image');
    }
  };

  const resetForm = () => {
    setImageUrl(null);
    setName('');
    setDescription('');
    setRelation('');
    setProcessing(false);  // Resume fetching new images
    fetchImage();  // Immediately fetch the next image or enter loading state
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#1E90FF" />
        <Text style={styles.loadingText}>Waiting for an image...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {imageUrl && (
        <Image source={{ uri: imageUrl }} style={styles.image} />
      )}

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Enter Name"
          placeholderTextColor="#aaa"
          value={name}
          onChangeText={setName}
        />
        <TextInput
          style={styles.input}
          placeholder="Enter Description"
          placeholderTextColor="#aaa"
          value={description}
          onChangeText={setDescription}
        />
        <TextInput
          style={styles.input}
          placeholder="Enter Relation"
          placeholderTextColor="#aaa"
          value={relation}
          onChangeText={setRelation}
        />
      </View>

      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.approveButton} onPress={handleApprove}>
          <Text style={styles.buttonText}>Approve</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.denyButton} onPress={handleDeny}>
          <Text style={styles.buttonText}>Deny</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
    backgroundColor: '#121212',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#fff',
    marginTop: 10,
  },
  image: {
    width: 300,
    height: 300,
    borderRadius: 10,
    marginBottom: 20,
  },
  buttonContainer: {
    flexDirection: 'row',
    gap: 20,
  },
  approveButton: {
    backgroundColor: '#28a745',
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 8,
  },
  denyButton: {
    backgroundColor: '#dc3545',
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 8,
  },
  submitButton: {
    backgroundColor: '#1E90FF',
    paddingVertical: 15,
    paddingHorizontal: 50,
    borderRadius: 8,
    marginTop: 20,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
  },
  inputContainer: {
    width: '100%',
    marginTop: 20,
  },
  input: {
    backgroundColor: '#1e1e1e',
    color: '#fff',
    paddingHorizontal: 15,
    paddingVertical: 10,
    borderRadius: 8,
    marginBottom: 15,
  },
});
