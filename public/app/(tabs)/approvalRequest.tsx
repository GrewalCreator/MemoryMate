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
  const [approved, setApproved] = useState<boolean | null>(null);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    fetchImage();
  }, []);

  const fetchImage = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://10.0.0.98:5000/api/get-image');
  
      if (response.status === 204) {
        setTimeout(fetchImage, 5000); // No image available, retry after 5 seconds
        return;
      }
  
      if (!response.ok) {
        throw new Error('Failed to fetch image');
      }
  
      const data = await response.json();
      if (data.image_url) {
        setImageUrl(data.image_url); // Set image URL directly
        setLoading(false);
      } else {
        setTimeout(fetchImage, 5000); // Retry if no image available
      }
    } catch (error) {
      console.error('Error fetching image:', error);
      setTimeout(fetchImage, 5000); // Retry fetching after failure
    }
  };
  

  const handleApprove = () => {
    setApproved(true);
  };

  const handleDeny = async () => {
    try {
      await fetch('http://10.0.0.98:5000/api/deny', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: 'deny' }),
      });
      Alert.alert('Denied', 'The image has been denied.');
      setApproved(null);
      fetchImage(); // Load next image
    } catch (error) {
      Alert.alert('Error', 'Failed to deny image');
    }
  };

  const handleSubmit = async () => {
    if (!name || !description) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    try {
      const response = await fetch('http://10.0.0.98:5000/api/approve', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, description, imageUrl }),
      });

      if (!response.ok) throw new Error('Failed to submit approval');

      Alert.alert('Success', 'The image has been approved.');
      setApproved(null);
      setName('');
      setDescription('');
      fetchImage(); // Load next image
    } catch (error) {
      Alert.alert('Error', 'Failed to submit approval');
    }
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

      {approved === null ? (
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.approveButton} onPress={handleApprove}>
            <Text style={styles.buttonText}>Approve</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.denyButton} onPress={handleDeny}>
            <Text style={styles.buttonText}>Deny</Text>
          </TouchableOpacity>
        </View>
      ) : (
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
          <TouchableOpacity style={styles.submitButton} onPress={handleSubmit}>
            <Text style={styles.buttonText}>Submit</Text>
          </TouchableOpacity>
        </View>
      )}
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
