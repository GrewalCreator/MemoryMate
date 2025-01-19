import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity,
  Alert,
  useColorScheme,
} from "react-native";
import { launchImageLibrary } from "react-native-image-picker";
import { Colors } from "@/constants/Colors";

const ProfilePage = () => {
  const [profileImage, setProfileImage] = useState(
    "https://www.shutterstock.com/image-vector/default-avatar-profile-icon-transparent-600nw-2463868853.jpg"
  );
  const colorScheme = useColorScheme();
  const isDarkMode = colorScheme === "dark";

  const selectImage = () => {
    launchImageLibrary(
      {
        mediaType: "photo",
        maxWidth: 300,
        maxHeight: 300,
        quality: 1,
      },
      (response) => {
        if (response.didCancel) {
          Alert.alert("Cancelled", "You cancelled selecting an image.");
        } else if (response.errorCode) {
          Alert.alert("Error", response.errorMessage || "An error occurred.");
        } else if (response.assets && response.assets.length > 0) {
          const selectedImage = response.assets[0]?.uri || "";
          setProfileImage(selectedImage);
        }
      }
    );
  };

  return (
    <View
      style={[
        styles.container,
        { backgroundColor: isDarkMode ? Colors.dark.background : Colors.light.background },
      ]}
    >
      {/* Profile Header */}
      <View style={styles.profileHeader}>
        <TouchableOpacity onPress={selectImage} style={styles.profileImageWrapper}>
          <Image source={{ uri: profileImage }} style={styles.profileImage} />
        </TouchableOpacity>
        <Text
          style={[
            styles.profileName,
            { color: isDarkMode ? Colors.dark.text : Colors.light.text },
          ]}
        >
          John Doe
        </Text>
      </View>

      {/* Options Section */}
      <View style={styles.optionsContainer}>
        <TouchableOpacity
          style={[
            styles.optionButton,
            { backgroundColor: isDarkMode ? Colors.dark.card : Colors.light.card },
          ]}
          onPress={() => Alert.alert("Change Password", "Navigating to change password...")}
        >
          <Text
            style={[
              styles.optionText,
              { color: isDarkMode ? Colors.dark.text : Colors.light.text },
            ]}
          >
            Change Password
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[
            styles.optionButton,
            { backgroundColor: isDarkMode ? Colors.dark.card : Colors.light.card },
          ]}
          onPress={() => Alert.alert("Edit Authorized Users", "Navigating to edit authorized users...")}
        >
          <Text
            style={[
              styles.optionText,
              { color: isDarkMode ? Colors.dark.text : Colors.light.text },
            ]}
          >
            Edit Authorized Users
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[
            styles.optionButton,
            { backgroundColor: "#ff4d4d" },
          ]}
          onPress={() => Alert.alert("Logout", "You have been logged out.")}
        >
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 50,
  },
  profileHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 40,
  },
  profileImageWrapper: {
    borderRadius: 40,
    overflow: "hidden",
    borderWidth: 2,
    borderColor: "#ccc",
    marginRight: 15,
  },
  profileImage: {
    width: 80,
    height: 80,
    resizeMode: "cover",
  },
  profileName: {
    fontSize: 24,
    fontWeight: "bold",
  },
  optionsContainer: {
    flex: 1,
    justifyContent: "flex-start",
  },
  optionButton: {
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 8,
    marginBottom: 15,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 3,
    borderWidth: 1,
    borderColor: "#444",
  },
  optionText: {
    fontSize: 16,
    fontWeight: "bold",
  },
  logoutText: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#ffffff",
  },
});

export default ProfilePage;
