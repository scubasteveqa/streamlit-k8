import streamlit as st
from kubernetes import client, config


# Function to load in-cluster Kubernetes config
def load_incluster_config():
    try:
        config.load_incluster_config()
        st.success("Kubernetes in-cluster config loaded successfully.")
    except Exception as e:
        st.error(f"Error loading Kubernetes in-cluster config: {e}")


# Function to list pods across all namespaces
def list_all_pods():
    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces(watch=False)
    return pods.items


# Streamlit UI
st.title("Kubernetes Pod Viewer")
st.markdown("Displays all pods across all namespaces with their IPs.")

# Load Kubernetes config
load_incluster_config()

# Button to trigger pod listing
if st.button("List All Pods"):
    try:
        pods = list_all_pods()
        if pods:
            st.subheader("Pods List")
            for pod in pods:
                st.write(
                    f"**Pod Name**: {pod.metadata.name}, "
                    f"**Namespace**: {pod.metadata.namespace}, "
                    f"**Pod IP**: {pod.status.pod_ip}"
                )
        else:
            st.info("No pods found.")
    except Exception as e:
        st.error(f"Error fetching pods: {e}")
