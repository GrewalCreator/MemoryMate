// Dashboard.tsx

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  Image,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  Alert,
  Dimensions,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

// Define TypeScript interface for the person data
interface Person {
  id?: number;
  images: string[];
  name: string;
  relation?: string;
  description?: string;
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
      const response = await fetch(`http://localhost:5000/get-images`);
      if (!response.ok) throw new Error('Failed to fetch data');

      const data = await response.json();

      if (Array.isArray(data)) {
        const formattedData: Person[] = data.map((person, index) => {
          // Initialize default values
          const name = person.name ? person.name.trim() : 'Unknown';
          const relation = person.relation ? person.relation.trim() : 'Unknown';
          const description = person.description
            ? person.description.trim()
            : 'No description available';

          // Process images
          let images: string[] = [];

          if (Array.isArray(person.images)) {
            person.images.forEach((imageString) => {
              if (typeof imageString === 'string') {
                // Remove trailing newline characters and split by newline if multiple URLs are present
                const cleanedString = imageString.replace(/\n/g, '').trim();
                if (cleanedString) {
                  const splitImages = cleanedString.split('http').filter(Boolean);
                  splitImages.forEach((img, imgIndex) => {
                    const url = img.startsWith('://') ? `http${img}` : `http://${img}`;
                    if (url.startsWith('http')) {
                      images.push(url);
                    }
                  });
                }
              }
            });
          }

          // Remove any potential duplicates and invalid URLs
          images = Array.from(new Set(images)).filter((url) => {
            return url.startsWith('http://') || url.startsWith('https://');
          });

          return {
            id: person.id || index,
            images,
            name,
            relation,
            description,
          };
        });

        setPeople(formattedData);
      } else {
        throw new Error('Invalid data format');
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
    <TouchableOpacity style={styles.card} activeOpacity={0.8}>
      {item.images.length > 0 ? (
        <Image
          source={{ uri: item.images[0] }}
          style={styles.image}
          resizeMode="cover"
          onError={(e) => {
            console.error(`Failed to load image for ${item.name}:`, e.nativeEvent.error);
          }}
        />
      ) : (
        <View style={[styles.image, styles.placeholder]}>
          <Ionicons name="image-off" size={40} color="#555" />
        </View>
      )}
      <View style={styles.cardContent}>
        <Text style={styles.name}>{item.name}</Text>
        {item.relation !== 'Unknown' && <Text style={styles.relation}>{item.relation}</Text>}
        <Text style={styles.description} numberOfLines={3}>
          {item.description}
        </Text>
      </View>
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
      <TouchableOpacity style={styles.refreshButton} onPress={fetchPeople} accessibilityLabel="Refresh">
        <Ionicons name="refresh" size={28} color="#fff" />
      </TouchableOpacity>

      <FlatList
        data={people}
        keyExtractor={keyExtractor}
        renderItem={renderItem}
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.listContainer}
        snapToAlignment="start"
        decelerationRate="fast"
        snapToInterval={Dimensions.get('window').width * 0.8 + 20} // Adjust based on card width and margin
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 60, // Adjusted to account for the refresh button
    paddingHorizontal: 10,
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
    fontSize: 16,
  },
  refreshButton: {
    position: 'absolute',
    top: 20,
    right: 20,
    backgroundColor: '#1E90FF',
    padding: 10,
    borderRadius: 30,
    zIndex: 1,
    elevation: 5,
  },
  listContainer: {
    paddingVertical: 20,
  },
  card: {
    backgroundColor: '#1e1e1e',
    borderRadius: 15,
    padding: 15,
    marginRight: 20,
    width: Dimensions.get('window').width * 0.8,
    shadowColor: '#000',
    shadowOpacity: 0.4,
    shadowOffset: { width: 0, height: 4 },
    shadowRadius: 6,
    elevation: 8,
  },
  image: {
    width: '100%',
    height: 180,
    borderRadius: 10,
    backgroundColor: '#333',
  },
  placeholder: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  cardContent: {
    marginTop: 15,
  },
  name: {
    fontSize: 22,
    color: '#fff',
    fontWeight: 'bold',
  },
  relation: {
    fontSize: 16,
    color: '#aaa',
    marginTop: 5,
  },
  description: {
    fontSize: 14,
    color: '#ccc',
    marginTop: 10,
    lineHeight: 20,
  },
});
