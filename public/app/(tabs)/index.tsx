import { Image, StyleSheet } from 'react-native';

import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

export default function HomeScreen() {
  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={
        <Image
          source={require('@/assets/images/MemoryMate-Logo.png')} // Replace with your product logo
          style={styles.productLogo}
        />
      }
    >
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title" style={styles.titleText}>
          About MemoryMate
        </ThemedText>
      </ThemedView>

      <ThemedView style={styles.sectionContainer}>
        <ThemedText type="subtitle" style={styles.subtitleText}>
          Our Mission
        </ThemedText>
        <ThemedText style={styles.bodyText}>
          MemoryMate is designed to empower individuals living with memory conditions like dementia to
          navigate their interactions with confidence. Our state-of-the-art glasses solution helps
          identify and log people you meet, making it easier to remember faces and foster connections.
        </ThemedText>
      </ThemedView>

      <ThemedView style={styles.sectionContainer}>
        <ThemedText type="subtitle" style={styles.subtitleText}>
          Features
        </ThemedText>
        <ThemedText style={styles.bodyText}>
          • Real-time identification of people you interact with.{'\n'}
          • Secure logging of identities for future reference.{'\n'}
          • Sleek and intuitive design tailored for ease of use.
        </ThemedText>
      </ThemedView>

      <ThemedView style={styles.sectionContainer}>
        <ThemedText type="subtitle" style={styles.subtitleText}>
          Who We Help
        </ThemedText>
        <ThemedText style={styles.bodyText}>
          MemoryMate is for anyone dealing with memory conditions, caregivers, or those seeking an easy,
          reliable way to recognize faces and names in their daily lives.
        </ThemedText>
      </ThemedView>

      <ThemedView style={styles.sectionContainer}>
        <ThemedText type="subtitle" style={styles.subtitleText}>
          Get in Touch
        </ThemedText>
        <ThemedText style={styles.bodyText}>
          Have questions or feedback? Contact us at{' '}
          <ThemedText type="defaultSemiBold" style={styles.contactText}>
            support@memorymate.com
          </ThemedText>
          .
        </ThemedText>
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  titleContainer: {
    alignItems: 'center',
    marginVertical: 16,
  },
  titleText: {
    fontSize: 28, // Larger title
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#4A90E2',
  },
  sectionContainer: {
    marginVertical: 16,
    paddingHorizontal: 16,
  },
  subtitleText: {
    fontSize: 24, // Larger subtitles
    fontWeight: '700',
    marginBottom: 8,
    color: '#F5F5F5', // Lighter color for better contrast
  },
  bodyText: {
    fontSize: 16,
    lineHeight: 24,
    color: '#CCCCCC', // Softer text for readability
    textAlign: 'justify',
  },
  contactText: {
    color: '#4A90E2',
    textDecorationLine: 'underline',
  },
  productLogo: {
    height: 400,
    width: 300,
    alignSelf: 'center',
    resizeMode: 'contain',
  },
});
