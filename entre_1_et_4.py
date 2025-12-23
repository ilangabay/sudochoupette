import streamlit as st

import data_preparation


instructions="""
    **Aloooors, comment ça marche ce jeu chatonnien ?**
    En fait, c'est comme quand le chaton te demande un chiffre pour choisir une guilde de dragon. Quand le chaton te demande entre 1 et 4, il a placé
    les guildes en fonction de la probabilité (estimée) que tu dises 1, 2, 3 ou 4, et le chaton essaye toujours d'avoir une des 2 bonnes guilde et veut éviter la mauvaise guilde.
    Donc ici, c'est un peu pareil, tu dois choisir entre 1 et 4, et recommencer et recommencer etc. A chaque fois que tu choisis, un algo chatonnien aura classé tes choix en fonction de leur proba estimée ("là je pense que le plus probable c'est 4, puis 2, puis 1 puis 3")
    Le principe c'est que si le choix de la choupette est réellement aléatoire, les prédictions de l'algo chatonien ne devraient pas surperformées...
    
    Maintenant le système de points : 
    L'algo chatonien gagne des points en fonction de ses prédictions :
    - 6 points (ouaiiiiis, bravo Chaton) si tu as choisi le plus probable
    - 5 points (ouaiiiis, supeeer) si tu as choisi le deuxième plus probable
    - 1 point (d'accord) pour le 3ème
    - 0 (pov chaton) pour la pire guilde
    
    La moyenne des points du chaton est calculée à chaque nouveau choix. Si la moyenne est au dessus de 3, alors l'algo chatonnien sur-performe, bravo chaton
    """
def entre_1_et_4 ():
    st.title("Entre 1 et 4")
    
    st.markdown(instructions)

    if 'sequence' not in st.session_state:
        st.session_state.sequence = []
    if 'total' not in st.session_state:
        st.session_state.total = 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("1"):
            st.session_state.sequence.append(1)
            points = data_preparation.compare_to_user_input(st.session_state.sequence)
            st.session_state.total += points
    with col2:
        if st.button("2"):
            st.session_state.sequence.append(2)
            points = data_preparation.compare_to_user_input(st.session_state.sequence)
            st.session_state.total += points
    with col3:
        if st.button("3"):
            st.session_state.sequence.append(3)
            points = data_preparation.compare_to_user_input(st.session_state.sequence)
            st.session_state.total += points
    with col4:
        if st.button("4"):
            st.session_state.sequence.append(4)
            points = data_preparation.compare_to_user_input(st.session_state.sequence)
            st.session_state.total += points

    if st.button("Réinitialiser"):
        st.session_state.sequence = []
        st.session_state.total = 0

    if st.session_state.sequence:
        points = data_preparation.compare_to_user_input(st.session_state.sequence)
        messages = {6: "Ouaiiiiis, bravo Chaton", 5: "Ouaiiis, supeer", 1: "D'accord...", 0: "pov chaton"}
        st.info(messages.get(points, ""))
        st.write(f"Total: {st.session_state.total}")
        moyenne=data_preparation.recalculate_average(st.session_state.sequence,st.session_state.total, points)
        st.write(f"Moyenne : {moyenne}")
        if moyenne > 3+2.5/len(st.session_state.sequence):
            st.write("Il est fort cet algorithme chatonien ! (Au dessus de 3 points en moyenne c'est une surperformance)")
