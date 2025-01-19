import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  Image,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  Alert
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

// Define TypeScript interface for the person data
interface Person {
  id?: number;
  imageUrl: string;
  name: string;
  relation: string;
  description: string;
}

export default function Dashboard() {
  const [people, setPeople] = useState<Person[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPeople();
  }, []);

  const fetchPeople = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/get-images');
      if (!response.ok) throw new Error('Failed to fetch data');

      const data = await response.json();

      if (Array.isArray(data) && data.every(person => 'id' in person && person.id !== undefined)) {
        setPeople(data);
      } else {
        throw new Error('Invalid data format: Missing ID field');
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to fetch data');
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Safely extract the key while ensuring no undefined values
  const keyExtractor = (item: Person, index: number) => {
    return item.id ? item.id.toString() : `person-${index}`;
  };

  const renderItem = ({ item }: { item: Person }) => (
    <TouchableOpacity style={styles.card}>
      <Image source={{ uri: item.imageUrl }} style={styles.image} />
      <Text style={styles.name}>{item.name}</Text>
      <Text style={styles.relation}>{item.relation}</Text>
      <Text style={styles.description}>{item.description}</Text>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#1E90FF" />
        <Text style={styles.loadingText}>Loading people...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Refresh Button in Top Right */}
      <TouchableOpacity style={styles.refreshButton} onPress={fetchPeople}>
        <Ionicons name="refresh" size={28} color="#fff" />
      </TouchableOpacity>

      <FlatList
        data={people}
        keyExtractor={keyExtractor}
        renderItem={renderItem}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
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
  refreshButton: {
    position: 'absolute',
    top: 40,
    right: 20,
    backgroundColor: '#1E90FF',
    padding: 10,
    borderRadius: 30,
    zIndex: 1,
  },
  card: {
    backgroundColor: '#1e1e1e',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.3,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 4,
    elevation: 5,
  },
  image: {
    width: 120,
    height: 120,
    borderRadius: 60,
    marginBottom: 10,
  },
  name: {
    fontSize: 20,
    color: '#fff',
    fontWeight: 'bold',
  },
  relation: {
    fontSize: 16,
    color: '#aaa',
    marginBottom: 5,
  },
  description: {
    fontSize: 14,
    color: '#ccc',
  },
  listContainer: {
    paddingBottom: 20,
  },
});

