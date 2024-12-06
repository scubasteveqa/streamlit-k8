import streamlit as st
from kubernetes import client, config

# Function to load Kubernetes config
def load_kube_config():
    try:
        config.load_kube_config()
        st.success("Kubernetes config loaded successfully.")
    except Exception as e:
        st.error(f"Error loading Kubernetes config: {e}")

# Function to list pods
def list_pods(namespace="default"):
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace=namespace)
    return pods.items

# Function to list services
def list_services(namespace="default"):
    v1 = client.CoreV1Api()
    services = v1.list_namespaced_service(namespace=namespace)
    return services.items

# Function to list deployments
def list_deployments(namespace="default"):
    apps_v1 = client.AppsV1Api()
    deployments = apps_v1.list_namespaced_deployment(namespace=namespace)
    return deployments.items

# Streamlit UI
st.title("Kubernetes Resource Viewer")

# Load Kubernetes config
load_kube_config()

namespace = st.text_input("Enter Namespace", value="default")

resource_type = st.selectbox("Select Resource Type", ["Pods", "Services", "Deployments"])

if st.button("List Resources"):
    if resource_type == "Pods":
        pods = list_pods(namespace)
        st.subheader("Pods")
        for pod in pods:
            st.write(f"Name: {pod.metadata.name}, Status: {pod.status.phase}")
    elif resource_type == "Services":
        services = list_services(namespace)
        st.subheader("Services")
        for service in services:
            st.write(f"Name: {service.metadata.name}, Type: {service.spec.type}")
    elif resource_type == "Deployments":
        deployments = list_deployments(namespace)
        st.subheader("Deployments")
        for deployment in deployments:
            st.write(f"Name: {deployment.metadata.name}, Replicas: {deployment.spec.replicas}")
