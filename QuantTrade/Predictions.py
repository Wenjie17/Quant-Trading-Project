'''
Make predictions with 4 models: Random Forest, Neural Network, SVM, Logistic Regressions
'''

def forest(xTr, yTr, xVa, yVa, m, md=np.inf):  # M: tree;
    n, d = xTr.shape
    trees = []
    scores = []
    for i in range(m):
        random_array = np.random.randint(n, size=n)
        my_xTr = xTr[random_array]
        my_yTr = yTr[random_array]
        this_tree = DecisionTreeClassifier(criterion='gini', min_samples_split=10, min_samples_leaf=round(10.0 / 3.0), max_depth=md)
        tree = this_tree.fit(my_xTr, my_yTr)
        score = this_tree.score(xVa, yVa)
        scores.append(score)
        trees.append(tree)
    return trees, scores


def evalforest(trees, X, alphas=None, threshold=0.5):
    m = len(trees)
    n, d = X.shape
    if alphas is None:
        alphas = np.ones(m) / len(trees)
    # pred = np.zeros(n)
    my_list = []
    for i in range(m):
        my_list.append(trees[i].predict(X))
    raw_preds = np.stack(my_list, axis=0)
    # print(raw_preds)
    # print(raw_preds.shape)
    transpose = raw_preds.T

    output = []
    for line in transpose:
        # Majority Votes
        # output.append(Counter(line).most_common(1))
        this_result = np.sum(line * alphas)
        if this_result > threshold:
            this_result = 1
        elif this_result < (-1 * threshold):
            this_result = -1
        else:
            this_result = 0
        output.append(this_result)
    pred = np.stack(output, axis=0)
    return pred


def Predict():
    SIGNALS = Signals.drop('Return', 1)
    SIGNALS = pd.concat([SIGNALS.iloc[:, 0], SIGNALS.iloc[:, 1:] * 2], axis=1)
    lag = 1
    X = SIGNALS.iloc[:-lag, 1:]
    Y = pd.DataFrame(SIGNALS.iloc[lag:, 0])
    T2 = int(len(SIGNALS) * 0.8)
    T1 = int(len(SIGNALS) * 0.6)
    Tr_X1 = X.iloc[0:T2, :]
    Tr_Y1 = Y.iloc[0:T2]
    Va_X1 = X.iloc[T2:, :]
    Va_Y1 = Y.iloc[T2:]
    final = deepcopy(Va_Y1)

# Logistic ---------------------------------------------------------------------------------------------------------
    Log = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial').fit(Tr_X1.values, Tr_Y1.values)
    pre_log = Log.predict(Va_X1)
    score_Log = Log.score(Va_X1, Va_Y1)
    final['Log_Predicted'] = pre_log
    # cm_log =ConfusionMatrix(final['Ret'], final['Log_Predicted'])

# Deep Learning - Neural Network -----------------------------------------------------------------------------------
    my_X = Tr_X1.values
    my_Y = Tr_Y1.values + 1  # >=0, catagorical
    my_Y = keras.utils.to_categorical(my_Y, num_classes=3)
    ev_X = Va_X1.values
    ev_Y = Va_Y1.values + 1
    ev_Y = keras.utils.to_categorical(ev_Y, num_classes=3)

    model_NN = Sequential()
    model_NN.add(Dense(50, activation='relu'))
    model_NN.add(Dense(3, activation='sigmoid'))
    fit = model_NN.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
    history = model_NN.fit(my_X, my_Y, epochs=50, batch_size=256, validation_data=(ev_X, ev_Y))
    scores = model_NN.evaluate(ev_X, ev_Y)
    # print('Validation Loss: {}\n Validation Accuracy: {}\n'.format(scores[0], scores[1]))
    pred_NN = model_NN.predict([ev_X], batch_size=10, verbose=1)
    pre_NN = pred_NN.argmax(axis=-1) - 1
    final['NN_Predicted'] = pre_NN
    # cm_NN =ConfusionMatrix(final['Ret'], final['NN_Predicted'])

# SVM --------------------------------------------------------------------------------------------------------------
    SVM = svm.SVC(gamma='scale', decision_function_shape='ovo').fit(Tr_X1.values, Tr_Y1.values)
    pre_SVM = SVM.predict(Va_X1)
    # score =  clf.score(Va_X, Va_Y)
    final['SVM_Predicted'] = pre_SVM
    # cm_SVM =ConfusionMatrix(final['Ret'], final['SVM_Predicted'])
    # cm_SVM.print_stats()

# Random Forest-----------------------------------------------------------------------------------------------------
    Tr_X2 = X.iloc[0:T1, :]
    Tr_Y2 = Y.iloc[0:T1]
    Va_X2 = X.iloc[T1:T2, :]
    Va_Y2 = Y.iloc[T1:T2]
    Te_X2 = X.iloc[T2:, :]
    Te_Y2 = Y.iloc[T2:]
    test, scores = forest(Tr_X2.values, Tr_Y2.values, Va_X2.values, Va_Y2.values, 10, md=20)
    pre_Tree = evalforest(test, Te_X2, np.array(scores), 0.4)
    # print(pre.shape)
    final['Forest_Predicted'] = pre_Tree
    # cm_RF =ConfusionMatrix(Forest['Ret'], final['Forest_Predicted'])

    return final


def decision(df):
    N = len(df)
    n = df.isna().sum()
    predict = deepcopy(SimpleSum['Ret'])
    predict.loc[:] = np.nan
    for t in range(n, N - 1):
        if df.iloc[t] >= 1.5:
            predict.iloc[t + 1] = 1
        elif df.iloc[t] <= - 1.5:
            predict.iloc[t + 1] = -1
        else:
            predict.iloc[t + 1] = 0
    return predict

